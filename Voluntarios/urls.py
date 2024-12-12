from django.urls import path
from . import views

urlpatterns = [
    path('programas/', views.gestion_programas, name='gestion_programas'),
    path('programas/crear/', views.crear_programa, name='crear_programa'),
    path('programas/editar/<int:programa_id>/', views.editar_programa, name='editar_programa'),
    path('programas/eliminar/<int:programa_id>/', views.eliminar_programa, name='eliminar_programa'),
]
