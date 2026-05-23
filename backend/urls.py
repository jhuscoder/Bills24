from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls import i18n
from django.conf import settings


urlpatterns = [
    path('', include('api.urls')),
    path('i18n/', include(i18n))
]