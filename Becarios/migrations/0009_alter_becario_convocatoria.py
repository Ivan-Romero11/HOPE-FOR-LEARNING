# Generated by Django 5.1 on 2024-10-06 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Becarios', '0008_becario_convocatoria'),
        ('Convocatorias', '0002_convocatoria_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='becario',
            name='convocatoria',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Convocatorias.convocatoria'),
        ),
    ]
