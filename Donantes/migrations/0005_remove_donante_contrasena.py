# Generated by Django 5.1 on 2024-11-11 02:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Donantes', '0004_rename_contraseña_donante_contrasena'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donante',
            name='contrasena',
        ),
    ]
