from django.urls import path

from Registro4 import views

urlpatterns = [
    path('Login4', views.registro4, name="Registro4"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]