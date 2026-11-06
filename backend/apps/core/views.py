"""Infrastructure endpoints."""

from django.db import connection
from django.http import JsonResponse


def health_check(request):
    """Liveness probe used by Render and uptime monitoring."""
    database_ok = True
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        database_ok = False

    status = 200 if database_ok else 503
    return JsonResponse(
        {"status": "ok" if database_ok else "degraded", "database": database_ok},
        status=status,
    )
