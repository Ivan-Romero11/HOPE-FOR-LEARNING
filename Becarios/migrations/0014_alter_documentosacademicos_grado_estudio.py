# Generated by Django 5.1 on 2024-11-26 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Becarios', '0013_alter_documentosacademicos_grado_estudio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentosacademicos',
            name='grado_estudio',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
