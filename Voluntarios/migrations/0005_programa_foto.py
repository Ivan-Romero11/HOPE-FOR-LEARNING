# Generated by Django 5.1 on 2024-12-10 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Voluntarios', '0004_inscripcion'),
    ]

    operations = [
        migrations.AddField(
            model_name='programa',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='programas_fotos/'),
        ),
    ]
