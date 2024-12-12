# financacion/models.py
from django.db import models
from Administradores.models import Administrador

class Gasto(models.Model):
    descripcion = models.TextField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_gasto = models.DateTimeField(auto_now_add=True)
    responsable = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    categoria_gasto = models.CharField(max_length=50)

    def __str__(self):
        return self.descripcion

class InformeTransparencia(models.Model):
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    total_donaciones = models.DecimalField(max_digits=15, decimal_places=2)
    total_gastos = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_final = models.DecimalField(max_digits=15, decimal_places=2)
    responsable = models.ForeignKey(Administrador, on_delete=models.CASCADE)

    def __str__(self):
        return f"Informe {self.fecha_generacion}"