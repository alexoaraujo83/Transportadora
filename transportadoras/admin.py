from django.contrib import admin
from .models import Transportadora
@admin.register(Transportadora)
class TransportadoraAdmin(admin.ModelAdmin):
    list_display=('id','__str__')
