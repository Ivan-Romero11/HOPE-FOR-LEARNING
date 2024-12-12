from django.urls import path
from . import views  # Importar las vistas

urlpatterns = [
    path('formulario/<int:id>/', views.formulario, name='formulario'),
    path('registro/', views.registro_becario, name='registro_becario'),
    path('Base', views.base, name='base'),
    path('Datos', views.seccdatos, name='seccdatos'),
    path('Mibeca', views.seccmibeca, name='seccmibeca'),
    path('Mis_calificaciones', views.seccmiscali, name='seccmiscali'),
    path('programas/', views.lista_programas, name='lista_programas'),
    path('programas/inscribir/<int:programa_id>/', views.inscribir_programa, name='inscribir_programa'),
]