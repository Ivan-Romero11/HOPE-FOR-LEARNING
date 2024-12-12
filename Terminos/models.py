from django.db import models

class Terminos(models.Model):
    # Define los campos de tu modelo aquí
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    # Agrega otros campos necesarios

    def __str__(self):
        return self.titulo
