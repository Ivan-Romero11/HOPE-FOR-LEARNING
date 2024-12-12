from django.contrib import admin
from .models import (
    Becario, Domicilio, EstatusDocumentacion, InformacionAcademica, InformacionBeca,
    EstadosBeca, RenovacionesBeca, EstudioSocioeconomico, DocumentosAcademicos
)

@admin.register(Becario)
class BecarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'fecha_registro', 'convocatoria')
    search_fields = ('usuario__nombre', 'convocatoria__nombre') 
    list_filter = ('convocatoria',)

@admin.register(Domicilio)
class DomicilioAdmin(admin.ModelAdmin):
    list_display = ('becario', 'direccion', 'ciudad', 'estado')
    search_fields = ('becario__usuario__nombre',)

@admin.register(InformacionAcademica)
class InformacionAcademicaAdmin(admin.ModelAdmin):
    list_display = (
        'becario', 
        'nivel_academico', 
        'institucion_educativa', 
        'carrera', 
        'promedio', 
        'fecha_ingreso', 
        'fecha_egreso', 
        'tipo_periodo',
        'grado'
    )
    search_fields = (
        'becario_usuario_nombre', 
        'becario_usuario_apellidos', 
        'carrera', 
        'institucion_educativa', 
        'grado',
        'tipo_periodo'
    )
    list_filter = (
        'nivel_academico', 
        'institucion_educativa', 
        'fecha_ingreso', 
        'fecha_egreso', 
        'grado',
        'tipo_periodo'
    )
    ordering = ('-fecha_ingreso',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('becario',)
        return self.readonly_fields

@admin.register(InformacionBeca)
class InformacionBecaAdmin(admin.ModelAdmin):
    list_display = ('becario', 'beca_asignada', 'monto_beca', 'fecha_inicio_beca', 'fecha_fin_beca')
    search_fields = ('becario__usuario__nombre',)

@admin.register(EstadosBeca)
class EstadosBecaAdmin(admin.ModelAdmin):
    list_display = ('becario', 'estado', 'fecha_cambio')
    search_fields = ('becario__usuario__nombre', 'estado')

@admin.register(RenovacionesBeca)
class RenovacionesBecaAdmin(admin.ModelAdmin):
    list_display = ('becario', 'fecha_renovacion', 'periodo', 'estado')
    search_fields = ('becario__usuario__nombre',)

@admin.register(EstudioSocioeconomico)
class EstudioSocioeconomicoAdmin(admin.ModelAdmin):
    list_display = ('becario', 'ingreso_mensual', 'numero_dependientes')
    search_fields = ('becario__usuario__nombre',)

@admin.register(DocumentosAcademicos)
class DocumentosAcademicosAdmin(admin.ModelAdmin):
    list_display = ('becario', 'grado_estudio', 'promedio_general', 'promedio_semestre')
    search_fields = ('becario__usuario__nombre', 'grado_estudio')
    list_filter = ('grado_estudio',)

@admin.register(EstatusDocumentacion)
class EstatusDocumentacionAdmin(admin.ModelAdmin):
    list_display = ('documentos_academicos', 'estatus_constancia', 'estatus_boleta', 'fecha_revision')
    search_fields = ('documentos_academicos__becario__usuario__nombre', 'estatus_constancia', 'estatus_boleta')