# Becarios/models.py
from django.db import models
from Usuarios.models import Usuario
from Convocatorias.models import Convocatoria

class Becario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    convocatoria = models.ForeignKey(Convocatoria, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Becario: {self.usuario.nombre}"


class Domicilio(models.Model):
    id = models.AutoField(primary_key=True)
    becario = models.OneToOneField(Becario, on_delete=models.CASCADE)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=50)

    def __str__(self):
        return f"Domicilio de {self.becario.usuario.nombre}"

class InformacionAcademica(models.Model):
    becario = models.OneToOneField(Becario, on_delete=models.CASCADE, primary_key=True)
    nivel_academico = models.CharField(max_length=50)
    institucion_educativa = models.CharField(max_length=100)
    carrera = models.CharField(max_length=100)
    promedio = models.DecimalField(max_digits=4, decimal_places=2)
    fecha_ingreso = models.DateField()
    fecha_egreso = models.DateField(null=True, blank=True)
    tipo_periodo = models.CharField(max_length=50)
    grado = models.IntegerField(null=True, blank=True)

    def _str_(self):
        return f"Información Académica de {self.becario.usuario.nombre}"

class InformacionBeca(models.Model):
    becario = models.OneToOneField(Becario, on_delete=models.CASCADE, primary_key=True)
    beca_asignada = models.CharField(max_length=100)
    monto_beca = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_inicio_beca = models.DateField()
    fecha_fin_beca = models.DateField()

    def __str__(self):
        return f"Información de Beca para {self.becario.usuario.nombre}"

class EstadosBeca(models.Model):
    id = models.AutoField(primary_key=True)
    becario = models.ForeignKey(Becario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField()

    def __str__(self):
        return f"Estado de Beca para {self.becario.usuario.nombre}"

class RenovacionesBeca(models.Model):
    id = models.AutoField(primary_key=True)
    becario = models.ForeignKey(Becario, on_delete=models.CASCADE)
    fecha_renovacion = models.DateTimeField(auto_now_add=True)
    periodo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    comentarios = models.TextField()

    def __str__(self):
        return f"Renovación de Beca para {self.becario.usuario.nombre}"

class EstudioSocioeconomico(models.Model):
    id = models.AutoField(primary_key=True)
    becario = models.ForeignKey(Becario, on_delete=models.CASCADE)
    ingreso_mensual = models.DecimalField(max_digits=15, decimal_places=2)
    numero_dependientes = models.IntegerField()
    vivienda = models.CharField(max_length=50)
    ocupacion_padres = models.CharField(max_length=50)
    nivel_educativo_padres = models.CharField(max_length=50)
    comentarios = models.TextField()

    def __str__(self):
        return f"Estudio Socioeconómico de {self.becario.usuario.nombre}"
    
class DocumentosAcademicos(models.Model):
    becario = models.OneToOneField(Becario, on_delete=models.CASCADE, primary_key=True)
    constancia = models.FileField(upload_to='documentos/constancias/', null=True, blank=True)
    boleta = models.FileField(upload_to='documentos/boletas/', null=True, blank=True)
    grado_estudio = models.IntegerField(null=True, blank=True) 
    promedio_general = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    promedio_semestre = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def _str_(self):
        return f"Documentos de {self.becario.usuario.nombre}"

class EstatusDocumentacion(models.Model):
    documentos_academicos = models.OneToOneField(DocumentosAcademicos, on_delete=models.CASCADE, primary_key=True)
    estatus_constancia = models.CharField(max_length=20)
    estatus_boleta = models.CharField(max_length=20)
    comentarios_constancia = models.TextField(blank=True, null=True)
    comentarios_boleta = models.TextField(blank=True, null=True)
    fecha_revision = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Estatus de Documentación de {self.documentos_academicos.becario.usuario.nombre}"