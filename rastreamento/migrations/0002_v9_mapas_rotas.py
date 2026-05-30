# Generated manually for Fusion Cargas Inteligente V9
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[('fretes','0001_initial'),('rastreamento','0001_initial')]
    operations=[
        migrations.AddField(model_name='eventorastreamento', name='tipo', field=models.CharField(choices=[('POSICAO','Posição'),('COLETA','Coleta'),('PARADA','Parada'),('TRANSITO','Em trânsito'),('DESCARGA','Descarga'),('OCORRENCIA','Ocorrência'),('FINALIZACAO','Finalização')], default='POSICAO', max_length=20)),
        migrations.AddField(model_name='eventorastreamento', name='velocidade_kmh', field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
        migrations.AddField(model_name='eventorastreamento', name='odometro_km', field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
        migrations.AddField(model_name='eventorastreamento', name='origem_evento', field=models.CharField(default='manual', max_length=40)),
        migrations.CreateModel(name='PontoRota', fields=[('id',models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('sequencia',models.PositiveIntegerField(default=1)),('nome',models.CharField(max_length=150)),('endereco',models.CharField(blank=True, max_length=255)),('latitude',models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),('longitude',models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),('previsto_em',models.DateTimeField(blank=True, null=True)),('realizado_em',models.DateTimeField(blank=True, null=True)),('concluido',models.BooleanField(default=False)),('criado_em',models.DateTimeField(auto_now_add=True)),('frete',models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos_rota', to='fretes.frete'))], options={'ordering':['frete','sequencia'],'unique_together':{('frete','sequencia')}}),
        migrations.CreateModel(name='PosicaoAtualFrete', fields=[('id',models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),('latitude',models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),('longitude',models.DecimalField(blank=True, decimal_places=7, max_digits=10, null=True)),('descricao',models.CharField(blank=True, max_length=255)),('velocidade_kmh',models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),('odometro_km',models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),('atualizado_em',models.DateTimeField(auto_now=True)),('frete',models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='posicao_atual', to='fretes.frete'))]),
    ]
