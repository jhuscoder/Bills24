from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls import i18n
from django.conf import settings
from health_check.views import  HealthCheckView
# v7WFymLzUBA6L_u3lRYEvwTIjGHRPvGWsvaM6oFNRFs


urlpatterns = [
    path('', include('api.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('i18n/', include(i18n)),
    path('admin/', admin.site.urls),
    path("health/", HealthCheckView.as_view(
            checks=[  # optional, default is all but 3rd party checks
                "health_check.Cache",
                "health_check.DNS",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                # 3rd party checks
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Memory",
            ]
    ), name="health_check"),
]