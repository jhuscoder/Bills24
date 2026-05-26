from django.urls import path
from .views import API
from django.urls import include


urlpatterns = [    
    path("", API.as_view(), name="api-health"),
    path('accounts/', include('apps.accounts.api.urls')),
    path('bill/', include('apps.Bill.api.urls')),
    # JWT token obtain removed to prevent returning refresh tokens; use /api/accounts/login/ instead
]