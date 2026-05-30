from django.db import models
from django.contrib.auth.models import User
class PerfilUsuario(models.Model):
    class Papel(models.TextChoices):
        ADMIN='ADMIN','Administrador'
        OPERADOR='OPERADOR','Operador'
        CLIENTE='CLIENTE','Cliente'
        MOTORISTA='MOTORISTA','Motorista'
        TRANSPORTADORA='TRANSPORTADORA','Transportadora'
    usuario=models.OneToOneField(User,on_delete=models.CASCADE, related_name='perfil')
    papel=models.CharField(max_length=30, choices=Papel.choices, default=Papel.OPERADOR)
    telefone=models.CharField(max_length=30, blank=True)
    ativo=models.BooleanField(default=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.usuario.username} - {self.papel}'
