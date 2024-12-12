# Generated by Django 5.1 on 2024-09-10 22:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Becarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InformacionAcademica',
            fields=[
                ('becario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Becarios.becario')),
                ('nivel_academico', models.CharField(max_length=50)),
                ('institucion_educativa', models.CharField(max_length=100)),
                ('carrera', models.CharField(max_length=100)),
                ('promedio', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='InformacionBeca',
            fields=[
                ('becario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='Becarios.becario')),
                ('beca_asignada', models.CharField(max_length=100)),
                ('monto_beca', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_inicio_beca', models.DateField()),
                ('fecha_fin_beca', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('contrasena', models.CharField(max_length=100)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('fecha_nacimiento', models.DateField()),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos/')),
                ('rol', models.CharField(max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='datospersonales',
            name='email',
            field=models.EmailField(default='2000-01-01', max_length=100, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datospersonales',
            name='fecha_nacimiento',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datospersonales',
            name='genero',
            field=models.CharField(default='2000-01-01', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datospersonales',
            name='nombre',
            field=models.CharField(default='2000-01-01', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='becario',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='datospersonales',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='domicilio',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='EstadosBeca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(max_length=20)),
                ('fecha_cambio', models.DateTimeField(auto_now_add=True)),
                ('comentarios', models.TextField()),
                ('becario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Becarios.becario')),
            ],
        ),
        migrations.CreateModel(
            name='EstudioSocioeconomico',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ingreso_mensual', models.DecimalField(decimal_places=2, max_digits=15)),
                ('numero_dependientes', models.IntegerField()),
                ('vivienda', models.CharField(max_length=50)),
                ('ocupacion_padres', models.CharField(max_length=50)),
                ('nivel_educativo_padres', models.CharField(max_length=50)),
                ('comentarios', models.TextField()),
                ('becario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Becarios.becario')),
            ],
        ),
        migrations.CreateModel(
            name='RenovacionesBeca',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_renovacion', models.DateTimeField(auto_now_add=True)),
                ('periodo', models.CharField(max_length=20)),
                ('estado', models.CharField(max_length=20)),
                ('comentarios', models.TextField()),
                ('becario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Becarios.becario')),
            ],
        ),
        migrations.CreateModel(
            name='Donante',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('monto_donado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_ultima_donacion', models.DateField()),
                ('informes_impacto', models.TextField()),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Becarios.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Coordinador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Becarios.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_asignacion', models.DateTimeField(auto_now_add=True)),
                ('departamento', models.CharField(max_length=50)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Becarios.usuario')),
            ],
        ),
        migrations.AlterField(
            model_name='becario',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Becarios.usuario'),
        ),
        migrations.CreateModel(
            name='Voluntario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('estado_actual', models.CharField(max_length=20)),
                ('tareas', models.TextField()),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Becarios.usuario')),
            ],
        ),
    ]