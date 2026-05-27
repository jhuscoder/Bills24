from django.urls import path
from .views import (
	RegisterView,
	ProfileView,
	LoginView,
	PasswordResetView,
	PasswordResetConfirmView,
	ChangePasswordView,
	UpdateProfileView,
    UserBalanceView,
)


urlpatterns = [
	path('register/', RegisterView.as_view(), name='accounts-register'),
	path('me/', ProfileView.as_view(), name='accounts-profile'),
	path('login/', LoginView.as_view(), name='accounts-login'),
    path('balance/', UserBalanceView.as_view(), name='accounts-balance'),
	path('password/reset/', PasswordResetView.as_view(), name='accounts-password-reset'),
	path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='accounts-password-reset-confirm'),
	path('password/change/', ChangePasswordView.as_view(), name='accounts-change-password'),
	path('profile/update/', UpdateProfileView.as_view(), name='accounts-profile-update'),
]