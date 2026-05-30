from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from .models import EventoSeguranca

class RateLimitMiddleware:
    """Rate limit simples por IP para login e APIs sensíveis."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.window = int(getattr(settings, 'RATE_LIMIT_WINDOW_SECONDS', 60))
        self.max_login = int(getattr(settings, 'RATE_LIMIT_LOGIN_PER_MINUTE', 5))
        self.max_api = int(getattr(settings, 'RATE_LIMIT_API_PER_MINUTE', 120))

    def __call__(self, request):
        ip = self._ip(request)
        path = request.path or ''
        limite = None
        escopo = None
        if path.startswith('/accounts/login') or path.startswith('/api/token'):
            limite = self.max_login; escopo='login'
        elif path.startswith('/api/'):
            limite = self.max_api; escopo='api'
        if limite:
            key=f'rl:{escopo}:{ip}:{timezone.now().strftime("%Y%m%d%H%M")}'
            count=cache.get(key,0)+1
            cache.set(key,count,self.window)
            if count > limite:
                EventoSeguranca.objects.create(tipo='RATE_LIMIT', severidade='ALTA', ip=ip, caminho=path, metodo=request.method, detalhe=f'Limite excedido: {count}/{limite}')
                if path.startswith('/api/'):
                    return JsonResponse({'detail':'Muitas tentativas. Aguarde e tente novamente.'}, status=429)
                return HttpResponse('Muitas tentativas. Aguarde e tente novamente.', status=429)
        response=self.get_response(request)
        if response.status_code in (401,403):
            EventoSeguranca.objects.create(usuario=request.user if request.user.is_authenticated else None, tipo='ACESSO_NEGADO', severidade='MEDIA', ip=ip, caminho=path, metodo=request.method, detalhe=f'Status {response.status_code}')
        return response

    def _ip(self, request):
        forwarded=request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR','0.0.0.0')
