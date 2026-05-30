from decimal import Decimal
from django.db import models
from fretes.models import Frete
from motoristas.models import Motorista

class InsightOperacional(models.Model):
    class Tipo(models.TextChoices):
        PRECO='PRECO','Preço'
        RISCO='RISCO','Risco'
        MARGEM='MARGEM','Margem'
        MOTORISTA='MOTORISTA','Motorista'
        PRAZO='PRAZO','Prazo'
    class Severidade(models.TextChoices):
        BAIXA='BAIXA','Baixa'
        MEDIA='MEDIA','Média'
        ALTA='ALTA','Alta'
        CRITICA='CRITICA','Crítica'
    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='insights', null=True, blank=True)
    tipo=models.CharField(max_length=20, choices=Tipo.choices)
    severidade=models.CharField(max_length=20, choices=Severidade.choices, default=Severidade.BAIXA)
    titulo=models.CharField(max_length=180)
    descricao=models.TextField()
    score=models.DecimalField(max_digits=7, decimal_places=2, default=0)
    resolvido=models.BooleanField(default=False)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.titulo

class ScoreMotorista(models.Model):
    motorista=models.OneToOneField(Motorista,on_delete=models.CASCADE, related_name='score_operacional')
    entregas=models.PositiveIntegerField(default=0)
    ocorrencias=models.PositiveIntegerField(default=0)
    atrasos=models.PositiveIntegerField(default=0)
    score=models.DecimalField(max_digits=7, decimal_places=2, default=Decimal('100.00'))
    atualizado_em=models.DateTimeField(auto_now=True)
    def recalcular(self):
        penalidade=(self.ocorrencias*8)+(self.atrasos*5)
        bonus=min(self.entregas*1, 10)
        self.score=max(Decimal('0'), min(Decimal('100'), Decimal('90')+Decimal(bonus)-Decimal(penalidade)))
        return self.score
    def save(self,*args,**kwargs):
        self.recalcular(); super().save(*args,**kwargs)
    def __str__(self): return f'{self.motorista} - {self.score}'

class PrevisaoFrete(models.Model):
    frete=models.OneToOneField(Frete,on_delete=models.CASCADE, related_name='previsao_inteligente')
    valor_sugerido_min=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_sugerido_ideal=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_sugerido_max=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    margem_prevista=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    risco_operacional=models.DecimalField(max_digits=7, decimal_places=2, default=0)
    explicacao=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    atualizado_em=models.DateTimeField(auto_now=True)
    def __str__(self): return f'Previsão frete {self.frete_id}'
