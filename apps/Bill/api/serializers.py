from ..models import BillService, BillTransaction
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers


class BillSerializers(ModelSerializer):
    class Meta:
        model = BillService
        fields = ("id", "name", "icon", "slug")


class BillTransactionSerializer(ModelSerializer):
    class Meta:
        model = BillTransaction
        fields = ("tx_id", "service", "amount", "external_reference", "status", "response", "created_at")


class PayRequestSerializer(Serializer):
    service = serializers.CharField()
    account = serializers.CharField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    metadata = serializers.DictField(required=False)


class ApiWrapperSerializer(Serializer):
    code = serializers.CharField()
    message = serializers.CharField()
    data = serializers.JSONField(required=False, allow_null=True)


class BalanceResponseSerializer(Serializer):
    balance = serializers.DecimalField(max_digits=12, decimal_places=2)
    currency = serializers.CharField(default='NGN')


class RequestIDSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)


class AirtimeRequestSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)
    phone = serializers.CharField()
    service_id = serializers.CharField()
    amount = serializers.IntegerField()


class DataPurchaseSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)
    phone = serializers.CharField()
    service_id = serializers.CharField()
    variation_id = serializers.CharField()


class VerifyCustomerSerializer(Serializer):
    customer_id = serializers.CharField()
    service_id = serializers.CharField()
    variation_id = serializers.CharField(required=False)


class ElectricityPurchaseSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)
    customer_id = serializers.CharField()
    service_id = serializers.CharField()
    variation_id = serializers.CharField()
    amount = serializers.IntegerField()


class BettingPurchaseSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)
    customer_id = serializers.CharField()
    service_id = serializers.CharField()
    amount = serializers.IntegerField()


class TVPurchaseSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)
    customer_id = serializers.CharField()
    service_id = serializers.CharField()
    variation_id = serializers.CharField()
    subscription_type = serializers.CharField(required=False)
    amount = serializers.IntegerField(required=False)


class EpinsPurchaseSerializer(Serializer):
    request_id = serializers.CharField(max_length=50, required=False)
    service_id = serializers.CharField()
    value = serializers.IntegerField()
    quantity = serializers.IntegerField()


class RequerySerializer(Serializer):
    request_id = serializers.CharField(max_length=50)


class VariationsQuerySerializer(Serializer):
    service_id = serializers.CharField(required=False)
