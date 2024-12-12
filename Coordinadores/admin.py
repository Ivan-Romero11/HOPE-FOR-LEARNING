from django.contrib import admin
from .models import Coordinador, Estado

@admin.register(Coordinador)
class CoordinadorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'departamento')
    search_fields = ('usuario__nombre', 'departamento')


@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('coordinador', 'estado', 'fecha_cambio')
    search_fields = ('coordinador__usuario__nombre', 'estado')
    list_filter = ('estado', 'fecha_cambio')