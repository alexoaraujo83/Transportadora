from django.conf import settings
from django.db import models
from django.utils import timezone

class EventoSeguranca(models.Model):
    class Severidade(models.TextChoices):
        BAIXA='BAIXA','Baixa'
        MEDIA='MEDIA','Média'
        ALTA='ALTA','Alta'
        CRITICA='CRITICA','Crítica'
    class Tipo(models.TextChoices):
        LOGIN_FALHA='LOGIN_FALHA','Falha de login'
        RATE_LIMIT='RATE_LIMIT','Rate limit'
        ACESSO_NEGADO='ACESSO_NEGADO','Acesso negado'
        WEBHOOK_INVALIDO='WEBHOOK_INVALIDO','Webhook inválido'
        ACAO_CRITICA='ACAO_CRITICA','Ação crítica'
        SISTEMA='SISTEMA','Sistema'
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    tipo = models.CharField(max_length=40, choices=Tipo.choices)
    severidade = models.CharField(max_length=20, choices=Severidade.choices, default=Severidade.MEDIA)
    ip = models.GenericIPAddressField(null=True, blank=True)
    caminho = models.CharField(max_length=255, blank=True)
    metodo = models.CharField(max_length=10, blank=True)
    detalhe = models.TextField(blank=True)
    metadados = models.JSONField(default=dict, blank=True)
    criado_em = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        ordering = ['-criado_em']
        indexes = [models.Index(fields=['tipo','severidade','criado_em'])]
        verbose_name='Evento de segurança'
        verbose_name_plural='Eventos de segurança'

    def __str__(self):
        return f'{self.tipo} - {self.severidade} - {self.criado_em:%d/%m/%Y %H:%M}'

class PoliticaAcesso(models.Model):
    perfil = models.CharField(max_length=40, db_index=True)
    modulo = models.CharField(max_length=80)
    pode_visualizar = models.BooleanField(default=True)
    pode_criar = models.BooleanField(default=False)
    pode_editar = models.BooleanField(default=False)
    pode_excluir = models.BooleanField(default=False)
    pode_exportar = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [('perfil','modulo')]
        verbose_name='Política de acesso'
        verbose_name_plural='Políticas de acesso'

    def __str__(self):
        return f'{self.perfil} -> {self.modulo}'
