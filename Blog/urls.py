from django.urls import path
from .views import aviso_privacidad
from Blog import views

urlpatterns = [
    path('', views.blog, name="Blog"),
    path('Seccion1', views.seccion1, name="seccion1"),
    path('Seccion2', views.seccion2, name="seccion2"),
    path('Seccion3', views.seccion3, name="seccion3"),
    path('Seccion4', views.seccion4, name="seccion4"),
    path('Seccion5', views.seccion5, name="seccion5"),
    path('Seccion6', views.seccion6, name="seccion6"),
    path('Seccion7', views.seccion7, name="seccion7"),
    path('Seccion8', views.seccion8, name="seccion8"),
    path('Seccion9', views.seccion9, name="seccion9"),
    path('Seccion10', views.seccion10, name="seccion10"),
    path('Seccion11', views.seccion11, name="seccion11"),
    path('Seccion12', views.seccion12, name="seccion12"),
    path('aviso-privacidad/', aviso_privacidad, name='aviso_privacidad'),
]