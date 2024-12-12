from django.urls import path

from Registro1 import views

urlpatterns = [
    path('', views.registro1, name="Registro1"),
]