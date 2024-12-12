from django.db import models
from Usuarios.models import Usuario
from Becarios.models import Becario

class Voluntario(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.usuario.nombre

class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    voluntario = models.ForeignKey(Voluntario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField()

    def __str__(self):
        return f"Estado de {self.voluntario.usuario.nombre}: {self.estado}"

class Programa(models.Model):
    nombre_programa = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estatus = models.CharField(max_length=20)
    becarios_inscritos = models.IntegerField(default=0)
    voluntario = models.ForeignKey(Voluntario, related_name="programas", on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='programas_fotos/', null=True, blank=True)

    def __str__(self):
        return f"Programa: {self.nombre_programa} - {self.estatus}"

class Inscripcion(models.Model):
    becario = models.ForeignKey(Becario, on_delete=models.CASCADE)
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.becario.usuario.nombre} inscrito en {self.programa.nombre_programa} el {self.fecha_inscripcion}"