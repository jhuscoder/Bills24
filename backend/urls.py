from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf.urls import i18n
from django.conf import settings
import asyncio
from . import health as health_views


def _sync_await_view(view):
    """Wrap a view callable and run its coroutine result with asyncio.run if needed.
    This ensures compatibility when Django calls the view synchronously but the
    view implementation is async and returns a coroutine.
    """
    def wrapper(request, *args, **kwargs):
        result = view(request, *args, **kwargs)
        if asyncio.iscoroutine(result):
            return asyncio.run(result)
        return result

    return wrapper
# v7WFymLzUBA6L_u3lRYEvwTIjGHRPvGWsvaM6oFNRFs


urlpatterns = [
    path('', include('api.urls')),
    path('health/', _sync_await_view(health_views.liveness), name='health-liveness'),
    path('readiness/', _sync_await_view(health_views.readiness), name='health-readiness'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('i18n/', include(i18n)),
    path('admin/', admin.site.urls),
]