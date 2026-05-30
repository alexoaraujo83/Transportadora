from django.db import models
class LogAuditoria(models.Model):
    usuario=models.CharField(max_length=150, blank=True)
    metodo=models.CharField(max_length=10)
    caminho=models.CharField(max_length=255)
    ip=models.GenericIPAddressField(null=True, blank=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.metodo} {self.caminho}'
