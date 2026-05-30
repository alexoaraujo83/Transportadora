from django.utils import timezone
from rest_framework import serializers, viewsets, permissions, decorators, response
from .models import Notificacao

class NotificacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notificacao
        fields='__all__'
        read_only_fields=['usuario','criada_em','lida_em','enviada_tempo_real']

class NotificacaoViewSet(viewsets.ModelViewSet):
    serializer_class=NotificacaoSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        qs=Notificacao.objects.filter(usuario=self.request.user)
        lida=self.request.query_params.get('lida')
        canal=self.request.query_params.get('canal')
        if lida in ('true','false'):
            qs=qs.filter(lida=(lida=='true'))
        if canal:
            qs=qs.filter(canal=canal)
        return qs

    @decorators.action(detail=True,methods=['post'])
    def marcar_lida(self,request,pk=None):
        n=self.get_object(); n.lida=True; n.lida_em=timezone.now(); n.save(update_fields=['lida','lida_em'])
        return response.Response({'ok':True})

    @decorators.action(detail=False,methods=['post'])
    def marcar_todas_lidas(self,request):
        total=self.get_queryset().filter(lida=False).update(lida=True,lida_em=timezone.now())
        return response.Response({'ok':True,'total':total})
