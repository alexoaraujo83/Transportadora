from django import forms
from .models import ChecklistOperacional, ConsultaRisco, DocumentoFrete, OcorrenciaOperacional, TarefaOperacional
class ChecklistOperacionalForm(forms.ModelForm):
    class Meta:
        model=ChecklistOperacional
        exclude=['frete']
class ConsultaRiscoForm(forms.ModelForm):
    class Meta:
        model=ConsultaRisco
        fields=['motorista','frete','status','protocolo','observacao']

class DocumentoFreteForm(forms.ModelForm):
    class Meta:
        model=DocumentoFrete
        fields=['frete','tipo','numero','arquivo_url','descricao','validado']

class OcorrenciaOperacionalForm(forms.ModelForm):
    class Meta:
        model=OcorrenciaOperacional
        fields=['frete','titulo','descricao','gravidade','status','responsavel','resolvido_em']

class TarefaOperacionalForm(forms.ModelForm):
    class Meta:
        model=TarefaOperacional
        fields=['frete','titulo','descricao','prazo','concluida','responsavel']
