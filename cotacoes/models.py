from django.db import models
class Cotacao(models.Model):
    solicitante=models.CharField(max_length=160)
    contato=models.CharField(max_length=120, blank=True)
    origem=models.CharField(max_length=160)
    destino=models.CharField(max_length=160)
    carga=models.CharField(max_length=160)
    peso_kg=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    cubagem_m3=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    valor_sugerido=models.DecimalField(max_digits=12, decimal_places=2, default=0)
    aprovada=models.BooleanField(default=False)
    criada_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'Cotação {self.origem} x {self.destino}'
