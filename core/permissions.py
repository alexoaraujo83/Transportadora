from rest_framework import permissions

class PapelRequiredMixin:
    papeis_permitidos = []
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            perfil = getattr(request.user, 'perfil', None)
            if self.papeis_permitidos and (not perfil or perfil.papel not in self.papeis_permitidos):
                from django.core.exceptions import PermissionDenied
                raise PermissionDenied('Usuário sem permissão para esta operação.')
        return super().dispatch(request, *args, **kwargs)

class IsAdminOperadorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if request.user and request.user.is_superuser:
            return True
        papel = getattr(getattr(request.user, 'perfil', None), 'papel', None)
        return papel in ['ADMIN', 'OPERADOR']
