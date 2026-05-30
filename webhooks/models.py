from django.db import models
class WebhookEvento(models.Model):
    origem=models.CharField(max_length=80)
    evento=models.CharField(max_length=120)
    payload=models.JSONField(default=dict)
    processado=models.BooleanField(default=False)
    criado_em=models.DateTimeField(auto_now_add=True)
    def __str__(self): return f'{self.origem}:{self.evento}'
