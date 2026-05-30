from django.db import connection
from django.http import JsonResponse
from django.utils import timezone


def healthcheck(request):
    database = 'ok'
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
    except Exception as exc:  # pragma: no cover
        database = f'erro: {exc.__class__.__name__}'
    status_code = 200 if database == 'ok' else 503
    return JsonResponse({
        'status': 'ok' if status_code == 200 else 'degraded',
        'database': database,
        'timestamp': timezone.now().isoformat(),
        'service': 'Fusion Cargas Inteligente',
        'version': 'V5',
    }, status=status_code)
