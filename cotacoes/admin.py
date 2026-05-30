from django.contrib import admin
from .models import Cotacao
@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display=('id','__str__')
