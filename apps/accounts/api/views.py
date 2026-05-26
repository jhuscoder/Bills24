from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from .serializers import UserBalanceSerializer, UserRegistrationSerializer, UserProfileSerializer
from api.response import success_response, error_response
from .serializers import (
	LoginSerializer,
	ChangePasswordSerializer,
	PasswordResetSerializer,
	PasswordResetConfirmSerializer,
	UpdateProfileSerializer,
)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from .serializers import TokenSerializer
from ipware import get_client_ip



class LoginView(APIView):
	permission_classes = [permissions.AllowAny]
	renderer_classes = [JSONRenderer]

	@extend_schema(
		request=LoginSerializer,
		responses=TokenSerializer
	)
	def post(self, request, *args, **kwargs):
		client_ip, is_routable = get_client_ip(request)
		serializer = LoginSerializer(
			data=request.data, 
			context={'ip_address': client_ip}
		)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		tokens = serializer.create_tokens(user)
		return success_response('Login successful', data=tokens)


class PasswordResetView(APIView):
	permission_classes = [permissions.AllowAny]
	renderer_classes = [JSONRenderer]

	@extend_schema(request=PasswordResetSerializer, responses=OpenApiResponse(response=OpenApiTypes.BOOL, description='Password reset email sent'))
	def post(self, request, *args, **kwargs):
		serializer = PasswordResetSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return success_response('Password reset email sent')


class PasswordResetConfirmView(APIView):
	permission_classes = [permissions.AllowAny]
	renderer_classes = [JSONRenderer]

	@extend_schema(request=PasswordResetConfirmSerializer, responses=OpenApiResponse(response=OpenApiTypes.BOOL, description='Password reset confirmation'))
	def post(self, request, *args, **kwargs):
		serializer = PasswordResetConfirmSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return success_response('Password has been reset')


class ChangePasswordView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	renderer_classes = [JSONRenderer]

	@extend_schema(request=ChangePasswordSerializer, responses=OpenApiResponse(response=OpenApiTypes.STR, description='Password change status'))
	def post(self, request, *args, **kwargs):
		serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
		serializer.is_valid(raise_exception=True)
		serializer.save()
		return success_response('Password changed successfully')


class UpdateProfileView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	renderer_classes = [JSONRenderer]

	@extend_schema(request=UpdateProfileSerializer, responses=UserProfileSerializer)
	def put(self, request, *args, **kwargs):
		serializer = UpdateProfileSerializer(instance=request.user, data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return success_response('Profile updated', data=UserProfileSerializer(user).data)


	@extend_schema(request=UpdateProfileSerializer, responses=UserProfileSerializer)
	def patch(self, request, *args, **kwargs):
		serializer = UpdateProfileSerializer(instance=request.user, data=request.data, partial=True)
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		return success_response('Profile updated', data=UserProfileSerializer(user).data)


class RegisterView(APIView):
	permission_classes = [permissions.AllowAny]
	renderer_classes = [JSONRenderer]

	@extend_schema(request=UserRegistrationSerializer, responses={201: UserProfileSerializer})
	def post(self, request, *args, **kwargs):
		serializer = UserRegistrationSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			user = serializer.save()
			return success_response('Account created', data=UserProfileSerializer(user).data, status_code=201)
		return error_response('Invalid data', data=serializer.errors, status_code=400)


class ProfileView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	renderer_classes = [JSONRenderer]

	@extend_schema(responses=UserProfileSerializer)
	def get(self, request, *args, **kwargs):
		serializer = UserProfileSerializer(request.user)
		return success_response('Profile retrieved', data=serializer.data)



class UserBalanceView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	renderer_classes = [JSONRenderer]

	@extend_schema(responses=UserBalanceSerializer)
	def get(self, request, *args, **kwargs):
		serializer = UserBalanceSerializer(request.user)
		return success_response('Balance retrieved', data=serializer.data)