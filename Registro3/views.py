from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from Donantes.models import Donante
from Donantes import views, urls

def registro3(request):
    # Verificar si el donante ya está autenticado
    if 'donante_id' in request.session:
        return redirect('base2')  # Redirige a la página base si ya está autenticado

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            email = form.cleaned_data['email']
            
            # Verificar si existe un donante con el nombre y correo proporcionados
            try:
                donante = Donante.objects.get(nombre=nombre, email=email)
                
                # Iniciar sesión para el donante
                request.session['donante_id'] = donante.id
                request.session['donante_nombre'] = donante.nombre


                return redirect('base2')  # Redirigir a la página base después de iniciar sesión
            except Donante.DoesNotExist:
                messages.error(request, 'No se encontró un donante con ese nombre y correo.')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = LoginForm()

    return render(request, 'Registro3/registro3.html', {'form': form})

def cerrar_sesion(request):
    # Eliminar todos los datos de la sesión
    request.session.flush()
    # Redirigir a la página de inicio
    return redirect('Home')
