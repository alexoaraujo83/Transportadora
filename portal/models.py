from django.db import models
from django.utils.crypto import get_random_string
from fretes.models import Frete

class TokenExterno(models.Model):
    class Tipo(models.TextChoices):
        CLIENTE='CLIENTE','Cliente'
        MOTORISTA='MOTORISTA','Motorista'
        PUBLICO='PUBLICO','Público'
    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='tokens_externos')
    tipo=models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.PUBLICO)
    token=models.CharField(max_length=80, unique=True, blank=True)
    ativo=models.BooleanField(default=True)
    expira_em=models.DateTimeField(null=True, blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        if not self.token:
            self.token=get_random_string(48)
        super().save(*args,**kwargs)
    def __str__(self): return f'{self.tipo} - frete {self.frete_id}'

class AceiteDigitalFrete(models.Model):
    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='aceites_digitais')
    nome=models.CharField(max_length=160)
    documento=models.CharField(max_length=40, blank=True)
    ip=models.GenericIPAddressField(null=True, blank=True)
    user_agent=models.TextField(blank=True)
    aceito=models.BooleanField(default=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Aceite {self.frete_id} - {self.nome}'

class ComprovantePortal(models.Model):
    class Tipo(models.TextChoices):
        COLETA='COLETA','Coleta'
        DESCARGA='DESCARGA','Descarga'
        PEDAGIO='PEDAGIO','Pedágio'
        OUTRO='OUTRO','Outro'
    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='comprovantes_portal')
    tipo=models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.OUTRO)
    descricao=models.CharField(max_length=180, blank=True)
    arquivo=models.FileField(upload_to='comprovantes/', null=True, blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.tipo} - frete {self.frete_id}'
