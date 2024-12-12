from django.contrib import admin
from .models import Voluntario, Estado, Programa

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ['usuario']  # Mostrar el campo usuario en la lista del admin
    search_fields = ['usuario__nombre']  # Permitir la búsqueda por nombre del usuario

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ['voluntario', 'estado', 'fecha_cambio', 'comentarios']  # Mostrar voluntario, estado, fecha de cambio y comentarios
    search_fields = ['voluntario__usuario__nombre', 'comentarios']  # Permitir la búsqueda por nombre del voluntario y comentarios
    list_filter = ['estado', 'fecha_cambio']  # Filtros para facilitar la navegación
    readonly_fields = ['fecha_cambio']  # La fecha de cambio es solo lectura, ya que se genera automáticamente

@admin.register(Programa)
class ProgramaAdmin(admin.ModelAdmin):
    list_display = ('nombre_programa', 'estatus', 'fecha_inicio', 'fecha_fin', 'becarios_inscritos', 'voluntario', 'foto')  # Campos a mostrar en la lista, incluyendo la foto
    list_filter = ('estatus', 'fecha_inicio', 'fecha_fin')  # Filtros por estatus y fechas
    search_fields = ('nombre_programa', 'descripcion', 'voluntario__usuario__nombre')  # Barra de búsqueda
    ordering = ('fecha_inicio',)  # Orden predeterminado
    date_hierarchy = 'fecha_inicio'  # Navegación por fechas