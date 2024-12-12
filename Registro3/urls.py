from django.urls import path

from Registro3 import views

urlpatterns = [
    path('Login2', views.registro3, name="Registro3"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]