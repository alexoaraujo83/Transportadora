from django import forms
from fretes.models import Frete
from motoristas.models import Motorista
from transportadoras.models import Transportadora
from cotacoes.models import Cotacao
from financeiro.models import LancamentoFinanceiro
from rastreamento.models import EventoRastreamento, PontoRota

class BootstrapModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            css='form-control'
            if isinstance(field.widget, (forms.CheckboxInput,)):
                css='form-check-input'
            field.widget.attrs.update({'class':css})

class FreteForm(BootstrapModelForm):
    class Meta:
        model=Frete; fields='__all__'; widgets={'data_coleta': forms.DateTimeInput(attrs={'type':'datetime-local'})}
class MotoristaForm(BootstrapModelForm):
    class Meta: model=Motorista; fields='__all__'
class TransportadoraForm(BootstrapModelForm):
    class Meta: model=Transportadora; fields='__all__'
class CotacaoForm(BootstrapModelForm):
    class Meta: model=Cotacao; fields='__all__'
class LancamentoFinanceiroForm(BootstrapModelForm):
    class Meta:
        model=LancamentoFinanceiro; fields='__all__'; widgets={'vencimento': forms.DateInput(attrs={'type':'date'})}
class EventoRastreamentoForm(BootstrapModelForm):
    class Meta: model=EventoRastreamento; fields='__all__'

class PontoRotaForm(BootstrapModelForm):
    class Meta:
        model=PontoRota
        fields='__all__'
        widgets={'previsto_em': forms.DateTimeInput(attrs={'type':'datetime-local'}), 'realizado_em': forms.DateTimeInput(attrs={'type':'datetime-local'})}
