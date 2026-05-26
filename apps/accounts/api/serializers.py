from rest_framework import serializers
from apps.accounts.models import Account
from .utils import Utils
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings


class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = (
			'user_id', 'email', 'first_name', 'last_name', 'phone', 'balance', 'date_joined'
		)


class UserRegistrationSerializer(serializers.Serializer):
	email = serializers.EmailField()
	first_name = serializers.CharField(required=False, allow_blank=True)
	last_name = serializers.CharField(required=False, allow_blank=True)
	phone = serializers.CharField(required=False, allow_blank=True)
	password = serializers.CharField(write_only=True)

	def validate_email(self, value):
		if Account.objects.filter(email=value).exists():
			raise serializers.ValidationError('A user with that email already exists.')
		return value

	def create(self, validated_data):
		password = validated_data.pop('password')
		user = Account.objects.create_user(
			email=validated_data.get('email'),
			password=password,
			first_name=validated_data.get('first_name', ''),
			last_name=validated_data.get('last_name', ''),
			phone=validated_data.get('phone', None),
		)
		# Send welcome email in a background thread; failures should not block creation
		try:
			Utils.send_mail_threaded({
				'subject': 'Welcome to Bills',
				'template_plain': 'emails/welcome.txt',
				'template_html': 'emails/welcome.html',
				'context': {'user': user},
			})
		except Exception:
			# swallow exceptions so registration still succeeds
			pass

		return user

	def to_representation(self, instance):
		return UserProfileSerializer(instance).data


class TokenSerializer(serializers.Serializer):
	access = serializers.CharField()


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(write_only=True)

	def validate(self, attrs):
		email = attrs.get('email')
		password = attrs.get('password')
		user = authenticate(username=email, password=password)
		if not user:
			raise serializers.ValidationError('Unable to log in with provided credentials.')
		if not user.is_active:
			raise serializers.ValidationError('User account is disabled.')
		attrs['user'] = user
		return attrs

	def create_tokens(self, user):
		access = AccessToken.for_user(user)
		return {
			'access': str(access),
		}


class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(write_only=True)
	new_password = serializers.CharField(write_only=True)

	def validate_old_password(self, value):
		user = self.context['request'].user
		if not user.check_password(value):
			raise serializers.ValidationError('Old password is not correct')
		return value

	def save(self, **kwargs):
		user = self.context['request'].user
		user.set_password(self.validated_data['new_password'])
		user.save()
		return user


class PasswordResetSerializer(serializers.Serializer):
	email = serializers.EmailField()

	def validate_email(self, value):
		if not Account.objects.filter(email=value).exists():
			raise serializers.ValidationError('No user is associated with this email address')
		return value

	def save(self):
		email = self.validated_data['email']
		user = Account.objects.get(email=email)
		uid = urlsafe_base64_encode(force_bytes(user.pk))
		token = default_token_generator.make_token(user)
		reset_url = f"{getattr(settings, 'NEXT_ROUTE', '')}/password/reset/confirm/{uid}/{token}"
		try:
			Utils.send_mail_threaded({
				'subject': 'Password reset',
				'template_plain': 'emails/password_reset.txt',
				'template_html': 'emails/password_reset.html',
				'context': {'user': user, 'reset_url': reset_url},
			})
		except Exception:
			pass
		return True


class PasswordResetConfirmSerializer(serializers.Serializer):
	uid = serializers.CharField()
	token = serializers.CharField()
	new_password = serializers.CharField(write_only=True)

	def validate(self, attrs):
		try:
			uid = force_str(urlsafe_base64_decode(attrs.get('uid')))
			user = Account.objects.get(pk=uid)
		except Exception:
			raise serializers.ValidationError('Invalid UID')

		if not default_token_generator.check_token(user, attrs.get('token')):
			raise serializers.ValidationError('Invalid or expired token')

		attrs['user'] = user
		return attrs

	def save(self):
		user = self.validated_data['user']
		user.set_password(self.validated_data['new_password'])
		user.save()
		return user


class UpdateProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = Account
		fields = ('first_name', 'last_name', 'phone')

	def update(self, instance, validated_data):
		for attr, value in validated_data.items():
			setattr(instance, attr, value)
		instance.save()
		return instance
