from django.db import models
from motoristas.models import Motorista
from transportadoras.models import Transportadora
class Frete(models.Model):
    class Status(models.TextChoices):
        ABERTO='ABERTO','Aberto'
        PROSPECTANDO='PROSPECTANDO','Prospectando'
        AGENDADO='AGENDADO','Agendado'
        EM_TRANSITO='EM_TRANSITO','Em trânsito'
        ENTREGUE='ENTREGUE','Entregue'
        CANCELADO='CANCELADO','Cancelado'
    origem=models.CharField(max_length=160)
    destino=models.CharField(max_length=160)
    carga=models.CharField(max_length=160)
    peso_kg=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cubagem_m3=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_motorista=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_cliente=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    forma_pagamento=models.CharField(max_length=120, blank=True)
    data_coleta=models.DateTimeField(null=True, blank=True)
    motorista=models.ForeignKey(Motorista,on_delete=models.SET_NULL,null=True,blank=True)
    transportadora=models.ForeignKey(Transportadora,on_delete=models.SET_NULL,null=True,blank=True)
    status=models.CharField(max_length=30, choices=Status.choices, default=Status.ABERTO)
    observacoes=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    atualizado_em=models.DateTimeField(auto_now=True)
    @property
    def margem(self): return self.valor_cliente - self.valor_motorista
    def __str__(self): return f'{self.origem} x {self.destino}'
