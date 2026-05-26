from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.accounts.api.serializers import UserProfileSerializer
from api.response import success_response, error_response
from ..models import BillService, BillTransaction
from .serializers import (
	BillSerializers,
	BillTransactionSerializer,
	PayRequestSerializer,
	ApiWrapperSerializer,
	BalanceResponseSerializer,
	RequestIDSerializer,
	AirtimeRequestSerializer,
	DataPurchaseSerializer,
	VerifyCustomerSerializer,
	ElectricityPurchaseSerializer,
	BettingPurchaseSerializer,
	TVPurchaseSerializer,
	EpinsPurchaseSerializer,
	RequerySerializer,
	VariationsQuerySerializer,
)
from .client import ExternalBillingClient
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
import uuid
import time
from decimal import Decimal, InvalidOperation
from django.db import transaction
from django.db.models import F


class ServiceListView(APIView):
	permission_classes = (AllowAny,)

	@extend_schema(request=None, responses=OpenApiResponse(response=BillSerializers(many=True), description='List of available bill services'))
	def get(self, request):
		services = BillService.objects.all()
		serializer = BillSerializers(services, many=True)
		return success_response('Services retrieved', data=serializer.data)


class PayBillView(APIView):
	permission_classes = (IsAuthenticated,)

	@extend_schema(request=PayRequestSerializer, responses=OpenApiResponse(response=BillTransactionSerializer, description='Payment initiation result'))
	def post(self, request):
		"""Initiate a bill payment to external provider.

		Expected payload: { service: <slug>, account: <account identifier>, amount: <decimal>, metadata: {...} }
		"""
		service_slug = request.data.get('service')
		account_ref = request.data.get('account')
		amount = request.data.get('amount')
		metadata = request.data.get('metadata', {})

		if not (service_slug and account_ref and amount):
			return error_response('Missing required parameters', status_code=400)

		service = get_object_or_404(BillService, slug=service_slug)

		# Verify user has enough balance before initiating
		try:
			req_amount = Decimal(str(amount))
		except Exception:
			req_amount = None

		if req_amount is not None and getattr(request.user, 'is_authenticated', False):
			if Decimal(str(request.user.balance)) < req_amount:
				return error_response('Insufficient funds', data={'code': 'insufficient_funds'}, status_code=402)

		# create a pending transaction
		tx = BillTransaction.objects.create(
			user=request.user,
			service=service,
			amount=amount,
			status=BillTransaction.STATUS_PENDING,
		)

		client = ExternalBillingClient()
		try:
			resp = client.pay(service_slug, amount, account_ref, metadata)
			# update transaction
			tx.external_reference = resp.get('reference') or resp.get('id')
			tx.response = resp
			tx.status = BillTransaction.STATUS_SUCCESS
			# debit user's balance based on returned amount_charged or request amount
			debit_amount = None
			data_block = resp.get('data') if isinstance(resp, dict) else None
			if data_block and isinstance(data_block, dict):
				amt = data_block.get('amount_charged') or data_block.get('amount')
				if amt is not None:
					try:
						debit_amount = Decimal(str(amt))
					except Exception:
						debit_amount = None
			if debit_amount is None:
				try:
					debit_amount = Decimal(str(amount))
				except Exception:
					debit_amount = None

			if debit_amount is not None and getattr(request.user, 'is_authenticated', False):
				with transaction.atomic():
					request.user.refresh_from_db()
					if Decimal(str(request.user.balance)) < debit_amount:
						# Cannot debit — mark failed and return error
						tx.status = BillTransaction.STATUS_FAILED
						tx.response = {'error': 'Insufficient funds at settlement'}
						tx.save()
						return error_response('Insufficient funds at settlement', data={'code': 'insufficient_funds'}, status_code=402)
					request.user.balance = F('balance') - debit_amount
					request.user.save(update_fields=['balance'])
					# save tx after successful debit
					tx.save()
			else:
				tx.save()
			return success_response('Payment successful', data={'transaction': str(tx.tx_id), 'provider': resp, 'request_id': payload.get('request_id') if 'payload' in locals() else None})
		except Exception as exc:
			tx.response = {'error': str(exc)}
			tx.status = BillTransaction.STATUS_FAILED
			tx.save()
			return error_response('Payment failed', data={'transaction': str(tx.tx_id), 'error': str(exc)}, status_code=502)


# --- External provider proxy endpoints guided by provided JSON spec ---
class ExternalProxyBase(APIView):
	permission_classes = (IsAuthenticated,)

	def call_provider_get(self, path, params=None):
		client = ExternalBillingClient()
		try:
			resp = client.get(path, params=params)
			return success_response('OK', data=resp)
		except Exception as exc:
			return error_response('External provider error', data={'error': str(exc)}, status_code=502)

	def call_provider_post(self, path, data):
		client = ExternalBillingClient()
		# prepare payload as a mutable dict (request.data can be QueryDict)
		if data is None:
			payload = {}
		elif hasattr(data, 'copy'):
			payload = data.copy()
		else:
			payload = dict(data)

		# auto-generate request_id for transactional endpoints if not provided
		if not path.endswith('requery'):
			if not payload.get('request_id'):
				payload['request_id'] = f"req_{int(time.time())}_{uuid.uuid4().hex[:8]}"

		# Determine required amount for pre-check (if possible)
		required_amount = None

		try:
			if 'amount' in payload and payload.get('amount') is not None:
				required_amount = Decimal(str(payload.get('amount')))
			elif path.endswith('epins'):
				# epins: value * quantity
				val = payload.get('value')
				qty = payload.get('quantity')
				if val is not None and qty is not None:
					required_amount = Decimal(str(val)) * Decimal(int(qty))
			elif path.endswith('data') and payload.get('variation_id'):
				# try to fetch variation price
				service = payload.get('service_id')
				variation_id = payload.get('variation_id')
				try:
					variations = client.get('api/v2/variations/data', params={'service_id': service} if service else None)
					# variations expected under variations['data'] or as list
					items = None
					if isinstance(variations, dict):
						items = variations.get('data') or variations
					elif isinstance(variations, list):
						items = variations
					if items:
						for it in items:
							if str(it.get('variation_id')) == str(variation_id):
								price = it.get('price') or it.get('amount')
								if price is not None:
									required_amount = Decimal(str(price))
				except Exception:
					# ignore variation lookup failures; will check after provider response
					pass
		except (InvalidOperation, ValueError): required_amount = None

		# Pre-check user balance if authenticated and we could determine an amount
		user = getattr(self.request, 'user', None)
		
		if user and getattr(user, 'is_authenticated', False) and required_amount is not None:
			current_balance = getattr(user, 'balance', None)
			try:
				if current_balance is not None and Decimal(str(current_balance)) < required_amount:
					return error_response('Insufficient funds', data={'code': 'insufficient_funds'}, status_code=402)
			except (InvalidOperation, ValueError):
				# fallback: allow provider call and handle debit after
				pass

		# Call external provider
		try:
			resp = client.post(path, payload)
		except Exception as exc:
			return error_response('External provider error', data={'error': str(exc)}, status_code=502)

		# If provider indicates success, debit user based on amount_charged or required_amount
		try:
			provider_ok = False
			data_block = None
			if isinstance(resp, dict):
				# Many responses use top-level 'code' == 'success' and nested 'data'
				if resp.get('code') == 'success':
					provider_ok = True
					data_block = resp.get('data')
				# Some providers return a direct dict with status
				if not data_block and 'status' in resp:
					provider_ok = resp.get('status') in ('completed-api', 'processing-api', 'initiated-api')
					data_block = resp

			# determine debit amount
			debit_amount = None
			if data_block and isinstance(data_block, dict):
				amt = data_block.get('amount_charged') or data_block.get('amount') or data_block.get('amount_charged')
				if amt is not None:
					debit_amount = Decimal(str(amt))

			# fallback to required_amount
			if debit_amount is None:
				debit_amount = required_amount

			if provider_ok and user and getattr(user, 'is_authenticated', False) and debit_amount is not None:
				with transaction.atomic():
					# refresh user balance and ensure enough funds
					user.refresh_from_db()
					if Decimal(str(user.balance)) < debit_amount:
						# provider succeeded but user lacks funds; attempt to refund later. For now return error
						return error_response('Insufficient funds at settlement', data={'code': 'insufficient_funds'}, status_code=402)
					# debit
					user.balance = F('balance') - debit_amount
					user.save(update_fields=['balance'])
					# create local transaction record when possible
					try:
						BillTransaction.objects.create(
							user=user,
							service=None,
							amount=debit_amount,
							external_reference=(data_block.get('order_id') if data_block else None) or resp.get('order_id') or resp.get('id') or resp.get('reference'),
							status=(data_block.get('status') if data_block else None) or 'success',
							response=resp,
						)
					except Exception:
						# ignore transaction save errors for now
						pass

		except Exception:
			# swallow any debit errors and return provider response
				pass

		# Attach request_id to returned data for client traceability
		try:
			if isinstance(resp, dict):
				resp_to_return = dict(resp)
				resp_to_return.setdefault('request_id', payload.get('request_id'))
			else:
				resp_to_return = {'response': resp, 'request_id': payload.get('request_id')}
		except Exception:
			resp_to_return = resp

		return success_response('OK', data=resp_to_return)



class APIv2RootView(ExternalProxyBase):
	permission_classes = (AllowAny,)

	@extend_schema(request=None, responses=OpenApiResponse(response=ApiWrapperSerializer, description='API v2 root descriptor'))
	def get(self, request):
		# minimal root descriptor
		return success_response('API v2 root', data={'namespace': 'api/v2'})



class BalanceView(ExternalProxyBase):
	@extend_schema(request=None, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Wallet balance retrieved'))
	def get(self, request):
		return self.call_provider_get('api/v2/balance')



class VerifyCustomerView(ExternalProxyBase):
	@extend_schema(request=VerifyCustomerSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Customer verification result'))
	def post(self, request):
		return self.call_provider_post('api/v2/verify-customer', request.data)



class AirtimeView(ExternalProxyBase):
	@extend_schema(request=AirtimeRequestSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Airtime purchase result'))
	def post(self, request):
		return self.call_provider_post('api/v2/airtime', request.data)


class VariationsDataView(ExternalProxyBase):
	permission_classes = (AllowAny,)

	@extend_schema(
		request=None,
		parameters=[OpenApiParameter('service_id', OpenApiTypes.STR, OpenApiParameter.QUERY, required=False)],
		responses=OpenApiResponse(response=ApiWrapperSerializer, description='Data variations list'),
	)
	def get(self, request):
		service_id = request.query_params.get('service_id')
		params = {'service_id': service_id} if service_id else None
		return self.call_provider_get('api/v2/variations/data', params=params)



class DataView(ExternalProxyBase):
	@extend_schema(request=DataPurchaseSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Data purchase result'))
	def post(self, request):
		return self.call_provider_post('api/v2/data', request.data)



class VariationsTVView(ExternalProxyBase):
	permission_classes = (AllowAny,)

	@extend_schema(
		request=None,
		parameters=[OpenApiParameter('service_id', OpenApiTypes.STR, OpenApiParameter.QUERY, required=False)],
		responses=OpenApiResponse(response=ApiWrapperSerializer, description='TV variations list'),
	)
	def get(self, request):
		service_id = request.query_params.get('service_id')
		params = {'service_id': service_id} if service_id else None
		return self.call_provider_get('api/v2/variations/tv', params=params)



class TVView(ExternalProxyBase):
	@extend_schema(request=TVPurchaseSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='TV subscription purchase result'))
	def post(self, request):
		return self.call_provider_post('api/v2/tv', request.data)



class ElectricityView(ExternalProxyBase):
	@extend_schema(request=ElectricityPurchaseSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Electricity purchase result'))
	def post(self, request):
		return self.call_provider_post('api/v2/electricity', request.data)



class BettingView(ExternalProxyBase):
	@extend_schema(request=BettingPurchaseSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Betting account funding result'))
	def post(self, request):
		return self.call_provider_post('api/v2/betting', request.data)



class EpinsView(ExternalProxyBase):
	@extend_schema(request=EpinsPurchaseSerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='ePINs purchase result'))
	def post(self, request):
		return self.call_provider_post('api/v2/epins', request.data)



class RequeryView(ExternalProxyBase):
	@extend_schema(request=RequerySerializer, responses=OpenApiResponse(response=ApiWrapperSerializer, description='Order requery result'))
	def post(self, request):
		return self.call_provider_post('api/v2/requery', request.data)
