# Generated by Django 5.1 on 2024-11-24 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Becarios', '0010_documentosacademicos_estatusdocumentacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentosacademicos',
            name='grado_estudio',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]