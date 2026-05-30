# Generated manually for Fusion Cargas Inteligente V4
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('financeiro', '0001_initial')]
    operations = [
        migrations.AddField(model_name='lancamentofinanceiro', name='categoria', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='lancamentofinanceiro', name='centro_custo', field=models.CharField(blank=True, max_length=80)),
        migrations.AddField(model_name='lancamentofinanceiro', name='data_pagamento', field=models.DateField(blank=True, null=True)),
        migrations.AddField(model_name='lancamentofinanceiro', name='observacao', field=models.TextField(blank=True)),
    ]
