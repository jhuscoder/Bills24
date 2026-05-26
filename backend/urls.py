from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls import i18n
from django.conf import settings
from health_check.views import MainView as HealthCheckView
# v7WFymLzUBA6L_u3lRYEvwTIjGHRPvGWsvaM6oFNRFs


urlpatterns = [
    path('', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('i18n/', include(i18n)),
    path('admin/', admin.site.urls),
    path("health/", HealthCheckView.as_view(), name="health_check"),
]