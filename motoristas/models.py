from django.db import models
class Motorista(models.Model):
    nome=models.CharField(max_length=160)
    cpf=models.CharField(max_length=20, blank=True)
    telefone=models.CharField(max_length=30, blank=True)
    antt=models.CharField(max_length=30, blank=True)
    placa=models.CharField(max_length=10, blank=True)
    veiculo=models.CharField(max_length=80, blank=True)
    carroceria=models.CharField(max_length=80, blank=True)
    aprovado_risco=models.BooleanField(default=False)
    ativo=models.BooleanField(default=True)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.nome
