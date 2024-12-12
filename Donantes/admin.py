# donantes/admin.py
from django.contrib import admin
from .models import Donante, Donacion

@admin.register(Donante)
class DonanteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'monto_donado', 'fecha_ultima_donacion')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'email')

@admin.register(Donacion)
class DonacionAdmin(admin.ModelAdmin):
    list_display = ('donante', 'monto', 'fecha_donacion', 'metodo_pago')
    search_fields = ('donante__nombre', 'monto')
    list_filter = ('fecha_donacion', 'metodo_pago')
