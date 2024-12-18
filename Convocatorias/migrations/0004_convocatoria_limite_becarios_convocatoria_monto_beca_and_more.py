# Generated by Django 5.1 on 2024-10-26 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Convocatorias', '0003_estado'),
    ]

    operations = [
        migrations.AddField(
            model_name='convocatoria',
            name='limite_becarios',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='convocatoria',
            name='monto_beca',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='convocatoria',
            name='presupuesto_limite_becarios',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=15, null=True),
        ),
    ]
