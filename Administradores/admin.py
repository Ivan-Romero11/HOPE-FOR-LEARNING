# administradores/admin.py
from django.contrib import admin
from .models import Administrador

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'departamento')
    search_fields = ('usuario__nombre', 'departamento')