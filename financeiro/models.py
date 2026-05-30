from decimal import Decimal
from django.db import models
from django.contrib.auth import get_user_model
from fretes.models import Frete
from motoristas.models import Motorista

User = get_user_model()

class LancamentoFinanceiro(models.Model):
    class Tipo(models.TextChoices):
        RECEITA='RECEITA','Receita'
        DESPESA='DESPESA','Despesa'
    frete=models.ForeignKey(Frete,on_delete=models.SET_NULL,null=True,blank=True)
    tipo=models.CharField(max_length=20, choices=Tipo.choices)
    descricao=models.CharField(max_length=180)
    valor=models.DecimalField(max_digits=12, decimal_places=2)
    categoria=models.CharField(max_length=80, blank=True)
    centro_custo=models.CharField(max_length=80, blank=True)
    vencimento=models.DateField(null=True, blank=True)
    data_pagamento=models.DateField(null=True, blank=True)
    pago=models.BooleanField(default=False)
    observacao=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.tipo} - {self.valor}'

class ContaFinanceira(models.Model):
    class Tipo(models.TextChoices):
        CAIXA='CAIXA','Caixa'
        BANCO='BANCO','Banco'
        CARTEIRA='CARTEIRA','Carteira digital'
    nome=models.CharField(max_length=120)
    tipo=models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.BANCO)
    banco=models.CharField(max_length=80, blank=True)
    agencia=models.CharField(max_length=30, blank=True)
    conta=models.CharField(max_length=40, blank=True)
    saldo_inicial=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ativa=models.BooleanField(default=True)
    criada_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nome

class ContaPagarReceber(models.Model):
    class Natureza(models.TextChoices):
        PAGAR='PAGAR','Conta a pagar'
        RECEBER='RECEBER','Conta a receber'
    class Status(models.TextChoices):
        ABERTA='ABERTA','Aberta'
        PARCIAL='PARCIAL','Parcial'
        BAIXADA='BAIXADA','Baixada'
        VENCIDA='VENCIDA','Vencida'
        CANCELADA='CANCELADA','Cancelada'
    frete=models.ForeignKey(Frete,on_delete=models.SET_NULL,null=True,blank=True, related_name='contas_financeiras')
    conta=models.ForeignKey(ContaFinanceira,on_delete=models.SET_NULL,null=True,blank=True)
    natureza=models.CharField(max_length=20, choices=Natureza.choices)
    descricao=models.CharField(max_length=180)
    documento=models.CharField(max_length=80, blank=True)
    favorecido=models.CharField(max_length=140, blank=True)
    valor_original=models.DecimalField(max_digits=12, decimal_places=2)
    valor_pago=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    vencimento=models.DateField()
    data_baixa=models.DateField(null=True, blank=True)
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.ABERTA)
    categoria=models.CharField(max_length=80, blank=True)
    centro_custo=models.CharField(max_length=80, blank=True)
    observacao=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    atualizado_em=models.DateTimeField(auto_now=True)
    @property
    def saldo(self): return (self.valor_original or Decimal('0')) - (self.valor_pago or Decimal('0'))
    def baixar(self, valor=None, data_baixa=None):
        from django.utils import timezone
        valor = Decimal(str(valor)) if valor is not None else self.saldo
        self.valor_pago = (self.valor_pago or Decimal('0')) + valor
        self.data_baixa = data_baixa or timezone.localdate()
        self.status = self.Status.BAIXADA if self.valor_pago >= self.valor_original else self.Status.PARCIAL
        self.save(update_fields=['valor_pago','data_baixa','status','atualizado_em'])
        return self
    def __str__(self): return f'{self.natureza} - {self.descricao}'

class RepasseMotorista(models.Model):
    class Status(models.TextChoices):
        PENDENTE='PENDENTE','Pendente'
        PROGRAMADO='PROGRAMADO','Programado'
        PAGO='PAGO','Pago'
        CANCELADO='CANCELADO','Cancelado'
    frete=models.OneToOneField(Frete,on_delete=models.CASCADE, related_name='repasse_motorista')
    motorista=models.ForeignKey(Motorista,on_delete=models.SET_NULL,null=True,blank=True)
    valor_frete=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    pedagio=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    adiantamento=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    descontos=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    data_programada=models.DateField(null=True, blank=True)
    data_pagamento=models.DateField(null=True, blank=True)
    observacao=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    atualizado_em=models.DateTimeField(auto_now=True)
    def recalcular(self):
        self.saldo=(self.valor_frete or Decimal('0'))+(self.pedagio or Decimal('0'))-(self.adiantamento or Decimal('0'))-(self.descontos or Decimal('0'))
        return self.saldo
    def save(self,*args,**kwargs):
        self.recalcular(); super().save(*args,**kwargs)
    def __str__(self): return f'Repasse {self.frete_id} - {self.status}'

class ComissaoOperacional(models.Model):
    class Status(models.TextChoices):
        PENDENTE='PENDENTE','Pendente'
        APROVADA='APROVADA','Aprovada'
        PAGA='PAGA','Paga'
        CANCELADA='CANCELADA','Cancelada'
    frete=models.ForeignKey(Frete,on_delete=models.CASCADE, related_name='comissoes')
    usuario=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    base_calculo=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    percentual=models.DecimalField(max_digits=5, decimal_places=2, default=0)
    valor=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    data_pagamento=models.DateField(null=True, blank=True)
    observacao=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def recalcular(self):
        self.valor=(self.base_calculo or Decimal('0'))*(self.percentual or Decimal('0'))/Decimal('100')
        return self.valor
    def save(self,*args,**kwargs):
        self.recalcular(); super().save(*args,**kwargs)
    def __str__(self): return f'Comissão {self.valor}'

class ConciliacaoBancaria(models.Model):
    class Status(models.TextChoices):
        PENDENTE='PENDENTE','Pendente'
        CONCILIADA='CONCILIADA','Conciliada'
        DIVERGENTE='DIVERGENTE','Divergente'
    conta=models.ForeignKey(ContaFinanceira,on_delete=models.CASCADE, related_name='conciliacoes')
    lancamento=models.ForeignKey(ContaPagarReceber,on_delete=models.SET_NULL,null=True,blank=True)
    data_movimento=models.DateField()
    historico=models.CharField(max_length=200)
    valor=models.DecimalField(max_digits=12, decimal_places=2)
    documento=models.CharField(max_length=80, blank=True)
    status=models.CharField(max_length=20, choices=Status.choices, default=Status.PENDENTE)
    observacao=models.TextField(blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.conta} - {self.valor}'

class FechamentoFinanceiro(models.Model):
    competencia=models.CharField(max_length=7, help_text='AAAA-MM')
    receitas=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    despesas=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    lucro_bruto=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    margem_percentual=models.DecimalField(max_digits=7, decimal_places=2, default=0)
    observacao=models.TextField(blank=True)
    fechado_por=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together=('competencia',)
    def __str__(self): return f'Fechamento {self.competencia}'
