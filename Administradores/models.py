# administradores/models.py
from django.db import models
from Usuarios.models import Usuario

class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)  # Referencia a Usuario
    departamento = models.CharField(max_length=50)

    def __str__(self):
        return self.usuario.nombre