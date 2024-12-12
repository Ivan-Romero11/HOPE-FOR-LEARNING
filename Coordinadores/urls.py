# Coordinadores/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('Actualizar-estado-becario/', actualizar_estado_becario, name='actualizar_estado_becario'),
    path('Becario/', lista_becarios, name='lista_becarios'),
    path('Convocatorias/', lista_convocatorias, name='lista_convocatorias'),
    path('Convocatorias/Ver', ver_convocatorias, name='ver_convocatorias'),
    path('convocatorias/editar/<int:id>/', editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/borrar/<int:id>/', borrar_convocatoria, name='borrar_convocatoria'),
    path('convocatorias/agregar/', agregar_convocatoria, name='agregar_convocatoria'),
    path('Coordinadores/', lista_coordinadores, name='lista_coordinadores'),
    path('coordinadores/editar/<int:pk>/', editar_coordinador, name='editar_coordinador'),
    path('Dashboard/', dashboard, name='dashboard'),
    path('Aceptados/', lista_becariosacep, name='lista_becariosacep'),
    path('Voluntarios/', voluntarios, name='voluntarios'),
    path('Voluntarios-Aceptados/', voluntarios_aceptados, name='voluntarios_aceptados'),
    path('Voluntarios-Rechazados/', voluntarios_rechazados, name='voluntarios_rechazados'),
    path('actualizar_estado_voluntario/', actualizar_estado_voluntario, name='actualizar_estado_voluntario'),
    path('Rechazados/', lista_becariosrecha, name='lista_becariosrecha'),
    path('cerrar_sesion/', cerrar_sesion, name='cerrar_sesion'),
    path('validar_documentos/', validar_documentos, name='validar_documentos'),
    path('actualizar_estatus_documento/', actualizar_estatus_documento, name='actualizar_estatus_documento'),
    path('programas/', programas, name='programas'),
    path('actualizar-estatus-programa/', actualizar_estatus_programa, name='actualizar_estatus_programa'),
]