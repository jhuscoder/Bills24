from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_GET
from django.core.cache import caches
from django.db import connections, DEFAULT_DB_ALIAS
import time


@require_GET
def liveness(request):
    """Liveness probe: extremely lightweight, returns 200 if the app process is up."""
    return HttpResponse("OK", status=200)


@require_GET
def readiness(request):
    """Readiness probe: checks DB and cache availability and reports status.

    Returns 200 when all checks pass, 503 when any check fails. Response is
    JSON with per-component results and a duration_ms field.
    """
    start = time.time()
    result = {"status": "ok", "checks": {}}

    # Database check
    try:
        conn = connections[DEFAULT_DB_ALIAS]
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        result["checks"]["database"] = {"ok": True}
    except Exception as exc:
        result["status"] = "degraded"
        result["checks"]["database"] = {"ok": False, "error": str(exc)}

    # Cache check (optional)
    try:
        cache = caches["default"]
        key = "health_check_ping"
        cache.set(key, "pong", timeout=5)
        val = cache.get(key)
        ok = val == "pong"
        result["checks"]["cache"] = {"ok": ok}
        if not ok:
            result["status"] = "degraded"
    except Exception as exc:
        result["status"] = "degraded"
        result["checks"]["cache"] = {"ok": False, "error": str(exc)}

    result["duration_ms"] = int((time.time() - start) * 1000)
    http_status = 200 if result["status"] == "ok" else 503
    return JsonResponse(result, status=http_status)
