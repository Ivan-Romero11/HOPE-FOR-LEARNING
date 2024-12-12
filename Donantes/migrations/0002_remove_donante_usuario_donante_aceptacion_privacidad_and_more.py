# Generated by Django 5.1 on 2024-10-24 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Donantes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donante',
            name='usuario',
        ),
        migrations.AddField(
            model_name='donante',
            name='aceptacion_privacidad',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donante',
            name='apellido_materno',
            field=models.CharField(default='N/A', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='apellido_paterno',
            field=models.CharField(default='N/A', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='autorizacion_datos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='donante',
            name='codigo_postal',
            field=models.CharField(default=28869, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='email',
            field=models.EmailField(default='rgregorio@ucol.mx', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='nombre',
            field=models.CharField(default='Null', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='persona_tipo',
            field=models.CharField(choices=[('Fisica', 'Persona Física'), ('Moral', 'Persona Moral')], default='F', max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='regimen_fiscal',
            field=models.CharField(default='Null', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donante',
            name='rfc',
            field=models.CharField(default='GDIJBNS46', max_length=13),
            preserve_default=False,
        ),
    ]