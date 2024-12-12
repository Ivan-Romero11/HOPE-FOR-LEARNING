from django.urls import path
from .views import *

# Define URL patterns for your views
urlpatterns = [
    path('Dashboard/', dashboard, name='dashboard_admi'),
    path('Convocatorias/Ver', ver_convocatorias, name='ver_convocatorias'),
    path('convocatorias/editar/<int:id>/', editar_convocatoria, name='editar_convocatoria'),
    path('convocatorias/borrar/<int:id>/', borrar_convocatoria, name='borrar_convocatoria'),
    path('convocatorias/agregar/', agregar_convocatoria, name='agregar_convocatoria'),
    path('Coordinadores/Activos/', lista_coordinadores, name='lista_coordinadores'),
    path('Coordinadores/Inactivos/', lista_coordinadores_inactivos, name='lista_coordinadores_inactivos'),
    path('Finanzas/', finanzas, name='finanzas'),
]