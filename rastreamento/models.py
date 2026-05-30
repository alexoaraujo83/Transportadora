from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from fretes.models import Frete

class EventoRastreamento(models.Model):
    class TipoEvento(models.TextChoices):
        POSICAO='POSICAO','Posição'
        COLETA='COLETA','Coleta'
        PARADA='PARADA','Parada'
        TRANSITO='TRANSITO','Em trânsito'
        DESCARGA='DESCARGA','Descarga'
        OCORRENCIA='OCORRENCIA','Ocorrência'
        FINALIZACAO='FINALIZACAO','Finalização'

    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='eventos')
    descricao=models.CharField(max_length=255)
    tipo=models.CharField(max_length=20, choices=TipoEvento.choices, default=TipoEvento.POSICAO)
    latitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True, validators=[MinValueValidator(-180), MaxValueValidator(180)])
    velocidade_kmh=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    odometro_km=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    origem_evento=models.CharField(max_length=40, default='manual')
    criado_em=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-criado_em']

    def __str__(self):
        return f'{self.frete} - {self.tipo} - {self.descricao}'

class PontoRota(models.Model):
    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='pontos_rota')
    sequencia=models.PositiveIntegerField(default=1)
    nome=models.CharField(max_length=150)
    endereco=models.CharField(max_length=255, blank=True)
    latitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    previsto_em=models.DateTimeField(null=True, blank=True)
    realizado_em=models.DateTimeField(null=True, blank=True)
    concluido=models.BooleanField(default=False)
    criado_em=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['frete','sequencia']
        unique_together=('frete','sequencia')

    def __str__(self):
        return f'{self.sequencia} - {self.nome}'

class PosicaoAtualFrete(models.Model):
    frete=models.OneToOneField(Frete,on_delete=models.CASCADE, related_name='posicao_atual')
    latitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude=models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    descricao=models.CharField(max_length=255, blank=True)
    velocidade_kmh=models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    odometro_km=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    atualizado_em=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Posição atual - {self.frete}'
