from django.urls import path
from . import views  # Importar las vistas

urlpatterns = [
    path('Base2', views.base2, name='base2'),
    path('reportes/', views.reporte, name='reportes'),
    path('reporte_pdf/<int:donante_id>/', views.reporte_pdf, name='reporte_pdf'),
    path('datos_donante/<int:donante_id>/', views.datos_donante, name='datos_donante'),
]