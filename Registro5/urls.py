from django.urls import path

from Registro5 import views

urlpatterns = [
    path('Login5', views.registro5, name="Registro5"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]