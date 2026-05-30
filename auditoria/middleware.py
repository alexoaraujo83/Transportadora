from .models import LogAuditoria
class AuditoriaMiddleware:
    def __init__(self, get_response): self.get_response=get_response
    def __call__(self, request):
        response=self.get_response(request)
        if not request.path.startswith('/static'):
            try:
                LogAuditoria.objects.create(usuario=getattr(request.user,'username','') if request.user.is_authenticated else '', metodo=request.method, caminho=request.path, ip=request.META.get('REMOTE_ADDR'))
            except Exception:
                pass
        return response
