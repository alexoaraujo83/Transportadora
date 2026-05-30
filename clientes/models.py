from django.db import models

class Cliente(models.Model):
    class TipoPessoa(models.TextChoices):
        PF = 'PF', 'Pessoa física'
        PJ = 'PJ', 'Pessoa jurídica'

    nome = models.CharField(max_length=180)
    tipo_pessoa = models.CharField(max_length=2, choices=TipoPessoa.choices, default=TipoPessoa.PJ)
    documento = models.CharField(max_length=32, blank=True, help_text='CPF ou CNPJ')
    telefone = models.CharField(max_length=40, blank=True)
    email = models.EmailField(blank=True)
    contato_principal = models.CharField(max_length=120, blank=True)
    origem_padrao = models.CharField(max_length=160, blank=True)
    observacoes = models.TextField(blank=True)
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        indexes = [models.Index(fields=['nome']), models.Index(fields=['documento'])]

    def __str__(self):
        return self.nome
