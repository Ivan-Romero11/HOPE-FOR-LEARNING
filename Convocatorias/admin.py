from django.contrib import admin
from .models import Convocatoria, RequisitoParticipacion, CategoriaParticipacion, DescripcionConvocatoria, Estado

@admin.register(Convocatoria)
class ConvocatoriaAdmin(admin.ModelAdmin):
    list_display = (
        'nombre', 'fecha_apertura', 'fecha_limite_inscripcion', 'fecha_resultados', 
        'monto_beca', 'presupuesto_limite_becarios', 'cantidad_becarios','foto'
    )
    search_fields = ('nombre',)
    list_filter = ('fecha_apertura', 'fecha_limite_inscripcion', 'fecha_resultados')

@admin.register(RequisitoParticipacion)
class RequisitoParticipacionAdmin(admin.ModelAdmin):
    list_display = ('convocatoria', 'requisito')
    search_fields = ('convocatoria__nombre',)
    list_filter = ('convocatoria__nombre',)

@admin.register(CategoriaParticipacion)
class CategoriaParticipacionAdmin(admin.ModelAdmin):
    list_display = ('convocatoria', 'categoria')
    search_fields = ('convocatoria__nombre',)
    list_filter = ('convocatoria__nombre',)

@admin.register(DescripcionConvocatoria)
class DescripcionConvocatoriaAdmin(admin.ModelAdmin):
    list_display = ('convocatoria', 'tipo', 'descripcion')
    search_fields = ('convocatoria__nombre', 'tipo')
    list_filter = ('convocatoria__nombre', 'tipo')

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('convocatoria', 'estado', 'fecha_cambio', 'comentarios')
    search_fields = ('convocatoria__nombre', 'estado')
    list_filter = ('estado', 'fecha_cambio')