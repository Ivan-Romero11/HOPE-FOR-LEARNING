# Generated by Django 5.1 on 2024-10-20 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Convocatorias', '0002_convocatoria_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=20)),
                ('fecha_cambio', models.DateTimeField(auto_now_add=True)),
                ('comentarios', models.TextField()),
                ('convocatoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Convocatorias.convocatoria')),
            ],
        ),
    ]
