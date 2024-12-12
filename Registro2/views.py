from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from Usuarios.models import Usuario
from Becarios.models import Becario
from django.contrib.auth.hashers import check_password

def registro2(request):
    # Verificar si el usuario ya está autenticado
    if 'usuario_id' in request.session:
        return redirect('base')  # Redirige a la página base si ya está autenticado

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            
            try:
                # Buscar el usuario por email
                usuario = Usuario.objects.get(email=email)
                
                # Verificar la contraseña
                if check_password(contrasena, usuario.contrasena):
                    # Verificar si el usuario está registrado como becario
                    try:
                        becario = Becario.objects.get(usuario=usuario)
                        # Establecer la sesión para el becario
                        request.session['usuario_id'] = usuario.id
                        request.session['usuario_nombre'] = usuario.nombre
                        request.session['es_becario'] = True  # Marca para indicar que es becario

                        return redirect('base')  # Redirigir a la página base si el login es exitoso
                    except Becario.DoesNotExist:
                        messages.error(request, 'Este usuario no está registrado como becario.')
                else:
                    messages.error(request, 'Credenciales Incorrectas.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciales Incorrectas.')
    else:
        form = LoginForm()

    return render(request, 'Registro2/registro2.html', {'form': form})


def cerrar_sesion(request):
    # Eliminar todos los datos de la sesión
    request.session.flush()
    # Redirigir a la página de inicio de sesión
    return redirect('Home')  # Cambia 'registro1' por el nombre correcto de tu vista de login si es diferente