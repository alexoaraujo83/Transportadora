from rest_framework.permissions import BasePermission
from .models import PoliticaAcesso

class PoliticaModuloPermission(BasePermission):
    """Permissão dinâmica por perfil e módulo para API."""
    modulo = None
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        perfil = getattr(getattr(request.user, 'perfil', None), 'papel', None) or getattr(request.user, 'papel', None) or 'OPERADOR'
        modulo = getattr(view, 'modulo_permissao', self.modulo or view.__class__.__name__.lower())
        try:
            pol = PoliticaAcesso.objects.get(perfil=perfil, modulo=modulo, ativo=True)
        except PoliticaAcesso.DoesNotExist:
            return request.method in ('GET','HEAD','OPTIONS')
        if request.method in ('GET','HEAD','OPTIONS'): return pol.pode_visualizar
        if request.method == 'POST': return pol.pode_criar
        if request.method in ('PUT','PATCH'): return pol.pode_editar
        if request.method == 'DELETE': return pol.pode_excluir
        return False
