# Generated by Django 5.1 on 2024-09-14 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Becarios', '0004_delete_datospersonales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='becario',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]