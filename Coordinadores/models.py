# Coordinadores/models.py
from django.db import models
from Usuarios.models import Usuario  # Importa el modelo Usuario desde la aplicación Usuarios


class Coordinador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.nombre
    
class Estado(models.Model):
    id = models.AutoField(primary_key=True)
    coordinador = models.ForeignKey(Coordinador, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20)
    fecha_cambio = models.DateTimeField(auto_now_add=True)
    comentarios = models.TextField()