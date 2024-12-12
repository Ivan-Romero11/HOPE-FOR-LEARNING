"""
URL configuration for appweb project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.utils.translation import activate
from django.contrib.auth import views as auth_views


from Inicio import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Inicio.urls')),
    path('Programas/', include('Programas.urls')),
    path('Nosotros/', include('Nosotros.urls')),
    path('Blog/', include('Blog.urls')),
    path('Becarios/', include('Becarios.urls')),
    path('Coordinadores/', include('Coordinadores.urls')),
    path('Convocatorias/', include('Convocatorias.urls')),
    path('Registro1/', include('Registro1.urls')),
    path('Registro2/', include('Registro2.urls')),
    path('Administradores/', include('Administradores.urls')),
    path('Registro3/', include('Registro3.urls')),
    path('Registro4/', include('Registro4.urls')),
    path('Registro5/', include('Registro5.urls')),
    path('Donantes/', include('Donantes.urls')),
    path('Terminos/', include('Terminos.urls')),
    path('Voluntarios/', include('Voluntarios.urls')),
    path('', include('Dm.urls')),
    # Recuperación de contraseña
       path('reset_password/', 
         auth_views.PasswordResetView.as_view(template_name='Registro1/password-reset.html'), 
         name='password_reset'),
         
    path('reset_password_send/', 
         auth_views.PasswordResetDoneView.as_view(template_name='Registro1/password_reset_done.html'), 
         name='password_reset_done'),
         
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='Registro1/password_reset_confirm.html'), 
         name='password_reset_confirm'),
         
    path('reset_password_complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='Registro1/password_reset_complete.html'), 
         name='password_reset_complete'),
    
]
def my_view(request):
    activate('en')  # Cambia el idioma al inglés.
    return render(request, 'inicio.html')
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)