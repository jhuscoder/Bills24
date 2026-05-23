from django.contrib import admin
from django.urls import path, include
from health_check.views import HealthCheckView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls import i18n
from django.conf import settings


urlpatterns = [
    path('', include('api.urls')),
    path(
        "health/",
        HealthCheckView.as_view(
            checks=[  
                # optional, default is all but 3rd party checks
                "health_check.Cache",
                # "health_check.DNS",
                "health_check.Database",
                "health_check.Mail",
                "health_check.Storage",
                 # 3rd party checks
                "health_check.contrib.psutil.CPU",
                "health_check.contrib.psutil.Memory",
                "health_check.contrib.psutil.Disk",
                "health_check.contrib.psutil.Memory",
            ]
        )
    ),
    path('i18n/', include(i18n))
]