from django.urls import path

from Terminos import views

urlpatterns = [
    path('', views.terminos, name="Terminos"),
]