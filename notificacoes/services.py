from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from .models import Notificacao

class NotificacaoService:
    @staticmethod
    def criar(usuario=None,titulo='',mensagem='',canal='sistema',prioridade='normal',link='',payload=None,enviar_tempo_real=True):
        notificacao=Notificacao.objects.create(
            usuario=usuario,titulo=titulo,mensagem=mensagem,canal=canal,prioridade=prioridade,link=link,payload=payload or {}
        )
        if enviar_tempo_real and usuario:
            NotificacaoService.enviar_websocket(notificacao)
        return notificacao

    @staticmethod
    def enviar_websocket(notificacao):
        channel_layer=get_channel_layer()
        if not channel_layer or not notificacao.usuario_id:
            return False
        payload={
            'tipo':'notificacao',
            'id':notificacao.id,
            'canal':notificacao.canal,
            'prioridade':notificacao.prioridade,
            'titulo':notificacao.titulo,
            'mensagem':notificacao.mensagem,
            'link':notificacao.link,
            'criada_em':notificacao.criada_em.isoformat(),
        }
        async_to_sync(channel_layer.group_send)(
            f'notificacoes_usuario_{notificacao.usuario_id}',
            {'type':'notificacao_evento','payload':payload}
        )
        notificacao.enviada_tempo_real=True
        notificacao.save(update_fields=['enviada_tempo_real'])
        return True

    @staticmethod
    def marcar_lida(notificacao):
        notificacao.lida=True
        notificacao.lida_em=timezone.now()
        notificacao.save(update_fields=['lida','lida_em'])
        return notificacao
