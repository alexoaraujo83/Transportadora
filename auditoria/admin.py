from django.contrib import admin
from .models import LogAuditoria
@admin.register(LogAuditoria)
class LogAuditoriaAdmin(admin.ModelAdmin):
    list_display=('id','__str__')
