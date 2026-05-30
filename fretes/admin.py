from django.contrib import admin
from .models import Frete
@admin.register(Frete)
class FreteAdmin(admin.ModelAdmin):
    list_display=('id','__str__')
