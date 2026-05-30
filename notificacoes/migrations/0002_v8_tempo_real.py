# Generated manually for Fusion Cargas Inteligente V8
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    dependencies=[('notificacoes','0001_initial'), migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations=[
        migrations.AddField('notificacao','usuario',models.ForeignKey(blank=True,null=True,on_delete=django.db.models.deletion.CASCADE,related_name='notificacoes',to=settings.AUTH_USER_MODEL)),
        migrations.AddField('notificacao','canal',models.CharField(choices=[('sistema','Sistema'),('frete','Frete'),('financeiro','Financeiro'),('seguranca','Segurança')],default='sistema',max_length=20)),
        migrations.AddField('notificacao','prioridade',models.CharField(choices=[('baixa','Baixa'),('normal','Normal'),('alta','Alta'),('critica','Crítica')],default='normal',max_length=20)),
        migrations.AddField('notificacao','link',models.CharField(blank=True,max_length=255)),
        migrations.AddField('notificacao','payload',models.JSONField(blank=True,default=dict)),
        migrations.AddField('notificacao','enviada_tempo_real',models.BooleanField(default=False)),
        migrations.AddField('notificacao','lida_em',models.DateTimeField(blank=True,null=True)),
        migrations.AlterModelOptions('notificacao',{'ordering':['-criada_em']}),
        migrations.AddIndex('notificacao',models.Index(fields=['usuario','lida'],name='notificaco_usuario_08dbe7_idx')),
        migrations.AddIndex('notificacao',models.Index(fields=['canal','prioridade'],name='notificaco_canal_1ef24d_idx')),
    ]
