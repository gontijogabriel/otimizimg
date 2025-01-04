# Generated by Django 5.1.4 on 2025-01-04 03:05

import django.db.models.deletion
import otimizimg.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otimizimg', '0004_alter_uploadedimage_options_uploadedimage_height_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='OptimizedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optimized_image', models.ImageField(help_text='Versão otimizada da imagem', upload_to='optimized/', validators=[otimizimg.validators.validate_image])),
                ('optimized_format', models.CharField(choices=[('JPEG', 'JPEG'), ('PNG', 'PNG'), ('WEBP', 'WebP')], help_text='Formato da imagem otimizada', max_length=10)),
                ('optimized_size', models.PositiveIntegerField(help_text='Tamanho otimizado em bytes')),
                ('width', models.IntegerField(default=0, editable=False, help_text='Largura da imagem otimizada em pixels')),
                ('height', models.IntegerField(default=0, editable=False, help_text='Altura da imagem otimizada em pixels')),
            ],
            options={
                'verbose_name': 'Imagem Otimizada',
                'verbose_name_plural': 'Imagens Otimizadas',
            },
        ),
        migrations.AlterModelOptions(
            name='uploadedimage',
            options={'ordering': ['-uploaded_at'], 'verbose_name': 'Imagem Original', 'verbose_name_plural': 'Imagens Originais'},
        ),
        migrations.RemoveField(
            model_name='uploadedimage',
            name='optimized_format',
        ),
        migrations.RemoveField(
            model_name='uploadedimage',
            name='optimized_image',
        ),
        migrations.RemoveField(
            model_name='uploadedimage',
            name='optimized_size',
        ),
        migrations.CreateModel(
            name='ImageRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('related_at', models.DateTimeField(auto_now_add=True, help_text='Data e hora da relação')),
                ('original_image', models.OneToOneField(help_text='Imagem original', on_delete=django.db.models.deletion.CASCADE, related_name='optimized_relation', to='otimizimg.uploadedimage')),
                ('optimized_image', models.OneToOneField(help_text='Imagem otimizada', on_delete=django.db.models.deletion.CASCADE, related_name='original_relation', to='otimizimg.optimizedimage')),
            ],
            options={
                'verbose_name': 'Relação de Imagem',
                'verbose_name_plural': 'Relações de Imagem',
            },
        ),
    ]
