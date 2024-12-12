from django.db import models

class Donante(models.Model):

    # Información personal del donante
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    email = models.EmailField()
    rfc = models.CharField(max_length=13)
    codigo_postal = models.CharField(max_length=10)

    # Persona física o moral
    persona_tipo = models.CharField(max_length=10, choices=[('Fisica', 'Persona Física'), ('Moral', 'Persona Moral')])

    # Régimen fiscal
    regimen_fiscal = models.CharField(max_length=100)

    # Información de donaciones
    monto_donado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_ultima_donacion = models.DateField()

    # Autorizaciones
    autorizacion_datos = models.BooleanField(default=False)
    aceptacion_privacidad = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} ({self.persona_tipo})"

class Donacion(models.Model):
    donante = models.ForeignKey(Donante, on_delete=models.CASCADE)
    
    # Información de la donación
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_donacion = models.DateTimeField(auto_now_add=True)
    
    # Método y referencia de pago
    metodo_pago = models.CharField(max_length=50)
    referencia_pago = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.donante.nombre} - {self.monto}"
