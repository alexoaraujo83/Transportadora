import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [('clientes', '0001_initial')]
    operations = [
        migrations.CreateModel(
            name='TabelaPrecoRota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origem', models.CharField(max_length=160)),
                ('destino', models.CharField(max_length=160)),
                ('veiculo', models.CharField(blank=True, max_length=80)),
                ('carroceria', models.CharField(blank=True, max_length=80)),
                ('valor_minimo_motorista', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('valor_sugerido_cliente', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('pedagio_estimado', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('custo_extra_estimado', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('margem_percentual', models.DecimalField(decimal_places=2, default=Decimal('15.00'), max_digits=5)),
                ('ativa', models.BooleanField(default=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['origem', 'destino']},
        ),
        migrations.CreateModel(
            name='PropostaComercial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origem', models.CharField(max_length=160)),
                ('destino', models.CharField(max_length=160)),
                ('carga', models.CharField(blank=True, max_length=180)),
                ('peso_kg', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('cubagem_m3', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('valor_motorista', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('valor_cliente', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('validade', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('RASCUNHO', 'Rascunho'), ('ENVIADA', 'Enviada'), ('APROVADA', 'Aprovada'), ('RECUSADA', 'Recusada'), ('CANCELADA', 'Cancelada')], default='RASCUNHO', max_length=20)),
                ('observacoes', models.TextField(blank=True)),
                ('criada_em', models.DateTimeField(auto_now_add=True)),
                ('atualizada_em', models.DateTimeField(auto_now=True)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientes.cliente')),
                ('rota', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='precificacao.tabelaprecorota')),
            ],
            options={'ordering': ['-criada_em']},
        ),
        migrations.AddIndex(model_name='tabelaprecorota', index=models.Index(fields=['origem', 'destino'], name='precificaca_origem_9dbfaa_idx')),
    ]
