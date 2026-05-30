from django.conf import settings
from django.db import models

class CanalNotificacao(models.TextChoices):
    SISTEMA='sistema','Sistema'
    FRETE='frete','Frete'
    FINANCEIRO='financeiro','Financeiro'
    SEGURANCA='seguranca','Segurança'

class PrioridadeNotificacao(models.TextChoices):
    BAIXA='baixa','Baixa'
    NORMAL='normal','Normal'
    ALTA='alta','Alta'
    CRITICA='critica','Crítica'

class Notificacao(models.Model):
    usuario=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True,related_name='notificacoes')
    canal=models.CharField(max_length=20,choices=CanalNotificacao.choices,default=CanalNotificacao.SISTEMA)
    prioridade=models.CharField(max_length=20,choices=PrioridadeNotificacao.choices,default=PrioridadeNotificacao.NORMAL)
    titulo=models.CharField(max_length=120)
    mensagem=models.TextField()
    link=models.CharField(max_length=255,blank=True)
    payload=models.JSONField(default=dict,blank=True)
    lida=models.BooleanField(default=False)
    enviada_tempo_real=models.BooleanField(default=False)
    criada_em=models.DateTimeField(auto_now_add=True)
    lida_em=models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering=['-criada_em']
        indexes=[models.Index(fields=['usuario','lida']),models.Index(fields=['canal','prioridade'])]

    def __str__(self):
        return self.titulo
