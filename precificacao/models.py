from decimal import Decimal
from django.db import models
from clientes.models import Cliente

class TabelaPrecoRota(models.Model):
    origem = models.CharField(max_length=160)
    destino = models.CharField(max_length=160)
    veiculo = models.CharField(max_length=80, blank=True)
    carroceria = models.CharField(max_length=80, blank=True)
    valor_minimo_motorista = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_sugerido_cliente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pedagio_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    custo_extra_estimado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    margem_percentual = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('15.00'))
    ativa = models.BooleanField(default=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['origem', 'destino']
        indexes = [models.Index(fields=['origem', 'destino'])]

    def __str__(self):
        return f'{self.origem} × {self.destino}'

    def calcular_valor_cliente(self):
        base = self.valor_minimo_motorista + self.pedagio_estimado + self.custo_extra_estimado
        if self.valor_sugerido_cliente > 0:
            return self.valor_sugerido_cliente
        return base * (Decimal('1') + (self.margem_percentual / Decimal('100')))

class PropostaComercial(models.Model):
    class Status(models.TextChoices):
        RASCUNHO = 'RASCUNHO', 'Rascunho'
        ENVIADA = 'ENVIADA', 'Enviada'
        APROVADA = 'APROVADA', 'Aprovada'
        RECUSADA = 'RECUSADA', 'Recusada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    rota = models.ForeignKey(TabelaPrecoRota, on_delete=models.SET_NULL, null=True, blank=True)
    origem = models.CharField(max_length=160)
    destino = models.CharField(max_length=160)
    carga = models.CharField(max_length=180, blank=True)
    peso_kg = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cubagem_m3 = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_motorista = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_cliente = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    validade = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.RASCUNHO)
    observacoes = models.TextField(blank=True)
    criada_em = models.DateTimeField(auto_now_add=True)
    atualizada_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-criada_em']

    @property
    def margem(self):
        return self.valor_cliente - self.valor_motorista

    def __str__(self):
        return f'Proposta #{self.id or "nova"} - {self.origem} × {self.destino}'
