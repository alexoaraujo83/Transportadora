from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=180)),
                ('tipo_pessoa', models.CharField(choices=[('PF', 'Pessoa física'), ('PJ', 'Pessoa jurídica')], default='PJ', max_length=2)),
                ('documento', models.CharField(blank=True, help_text='CPF ou CNPJ', max_length=32)),
                ('telefone', models.CharField(blank=True, max_length=40)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('contato_principal', models.CharField(blank=True, max_length=120)),
                ('origem_padrao', models.CharField(blank=True, max_length=160)),
                ('observacoes', models.TextField(blank=True)),
                ('ativo', models.BooleanField(default=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
            options={'ordering': ['nome']},
        ),
        migrations.AddIndex(model_name='cliente', index=models.Index(fields=['nome'], name='clientes_cl_nome_39b21d_idx')),
        migrations.AddIndex(model_name='cliente', index=models.Index(fields=['documento'], name='clientes_cl_doc_441fae_idx')),
    ]
