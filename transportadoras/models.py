from django.db import models
class Transportadora(models.Model):
    nome=models.CharField(max_length=160)
    cnpj=models.CharField(max_length=20, blank=True)
    telefone=models.CharField(max_length=30, blank=True)
    email=models.EmailField(blank=True)
    rntrc=models.CharField(max_length=30, blank=True)
    ativa=models.BooleanField(default=True)
    criada_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nome
