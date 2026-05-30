from django import forms
from .models import TabelaPrecoRota, PropostaComercial

class TabelaPrecoRotaForm(forms.ModelForm):
    class Meta:
        model = TabelaPrecoRota
        fields = '__all__'

class PropostaComercialForm(forms.ModelForm):
    class Meta:
        model = PropostaComercial
        fields = '__all__'
