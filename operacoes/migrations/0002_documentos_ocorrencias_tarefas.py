# Generated manually for Fusion Cargas Inteligente V4
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fretes', '0001_initial'),
        ('operacoes', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='DocumentoFrete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('CTE', 'CT-e'), ('NFE', 'NF-e'), ('COMPROVANTE_COLETA', 'Comprovante de coleta'), ('COMPROVANTE_DESCARGA', 'Comprovante de descarga'), ('OUTRO', 'Outro')], default='OUTRO', max_length=40)),
                ('numero', models.CharField(blank=True, max_length=80)),
                ('arquivo_url', models.URLField(blank=True)),
                ('descricao', models.TextField(blank=True)),
                ('validado', models.BooleanField(default=False)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('frete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documentos', to='fretes.frete')),
            ],
            options={'ordering': ['-criado_em']},
        ),
        migrations.CreateModel(
            name='OcorrenciaOperacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=160)),
                ('descricao', models.TextField()),
                ('gravidade', models.CharField(choices=[('BAIXA', 'Baixa'), ('MEDIA', 'Média'), ('ALTA', 'Alta'), ('CRITICA', 'Crítica')], default='MEDIA', max_length=20)),
                ('status', models.CharField(choices=[('ABERTA', 'Aberta'), ('EM_TRATATIVA', 'Em tratativa'), ('RESOLVIDA', 'Resolvida'), ('CANCELADA', 'Cancelada')], default='ABERTA', max_length=20)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('resolvido_em', models.DateTimeField(blank=True, null=True)),
                ('frete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ocorrencias', to='fretes.frete')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['-criado_em']},
        ),
        migrations.CreateModel(
            name='TarefaOperacional',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=160)),
                ('descricao', models.TextField(blank=True)),
                ('prazo', models.DateTimeField(blank=True, null=True)),
                ('concluida', models.BooleanField(default=False)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
                ('frete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tarefas', to='fretes.frete')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={'ordering': ['concluida', 'prazo', '-criado_em']},
        ),
    ]
