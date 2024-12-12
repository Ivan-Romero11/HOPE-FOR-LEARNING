from django.db import models

class Becario(models.Model):
    nombre = models.CharField(max_length=100)
    datos_personales = models.TextField()
    domicilio = models.TextField()
    estado_beca = models.CharField(max_length=50)
    estudio_socioeconomico = models.TextField()
    informacion_academica = models.TextField()
    informacion_beca = models.TextField()
    renovaciones_beca = models.TextField()

    def __str__(self):
        return self.nombre
