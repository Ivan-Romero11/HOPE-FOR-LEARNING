# Generated by Django 5.1 on 2024-10-26 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Convocatorias', '0005_convocatoria_cantidad_becarios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convocatoria',
            name='limite_becarios',
        ),
    ]
