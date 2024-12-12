from django.urls import path

from Registro2 import views

urlpatterns = [
    path('Login', views.registro2, name="Registro2"),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]