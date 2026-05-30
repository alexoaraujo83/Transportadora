# Generated manually for Fusion Cargas Inteligente V3
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fretes', '0001_initial'),
        ('motoristas', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='ChecklistOperacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentos_motorista', models.BooleanField(default=False)),
                ('risco_aprovado', models.BooleanField(default=False)),
                ('coleta_confirmada', models.BooleanField(default=False)),
                ('comprovante_coleta', models.BooleanField(default=False)),
                ('em_transito_confirmado', models.BooleanField(default=False)),
                ('descarga_confirmada', models.BooleanField(default=False)),
                ('comprovante_descarga', models.BooleanField(default=False)),
                ('financeiro_conferido', models.BooleanField(default=False)),
                ('ocorrencias_pendentes', models.BooleanField(default=False)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('frete', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='checklist', to='fretes.frete')),
            ],
        ),
        migrations.CreateModel(
            name='ConsultaRisco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('PENDENTE', 'Pendente'), ('APROVADO', 'Aprovado'), ('REPROVADO', 'Reprovado'), ('BLOQUEADO', 'Bloqueado')], default='PENDENTE', max_length=20)),
                ('protocolo', models.CharField(blank=True, max_length=80)),
                ('observacao', models.TextField(blank=True)),
                ('payload', models.JSONField(blank=True, default=dict)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('frete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultas_risco', to='fretes.frete')),
                ('motorista', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas_risco', to='motoristas.motorista')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricoStatusFrete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_anterior', models.CharField(blank=True, max_length=30)),
                ('status_novo', models.CharField(max_length=30)),
                ('observacao', models.TextField(blank=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('frete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_status', to='fretes.frete')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-criado_em']},
        ),
    ]
