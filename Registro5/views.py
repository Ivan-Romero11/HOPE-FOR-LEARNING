from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from Usuarios.models import Usuario
from Voluntarios.models import Voluntario
from django.contrib.auth.hashers import check_password

def registro5(request):
    # Verificar si el usuario ya está autenticado
    if 'usuario_id' in request.session:
        return redirect('gestion_programas')  # Redirige a la página base si ya está autenticado

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
                    # Verificar si el usuario está registrado como voluntario
                    try:
                        voluntario = Voluntario.objects.get(usuario=usuario)
                        
                        # Establecer la sesión para el voluntario
                        request.session['usuario_id'] = usuario.id
                        request.session['voluntario_id'] = voluntario.id  # Guardar el ID del voluntario
                        request.session['usuario_nombre'] = usuario.nombre
                        request.session['es_voluntario'] = True  # Marca para indicar que es voluntario

                        return redirect('gestion_programas')  # Redirigir a la página base si el login es exitoso
                    except Voluntario.DoesNotExist:
                        messages.error(request, 'Este usuario no está registrado como voluntario.')
                else:
                    messages.error(request, 'Credenciales Incorrectas.')
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciales Incorrectas.')
    else:
        form = LoginForm()

    return render(request, 'Registro5/registro5.html', {'form': form})



def cerrar_sesion(request):
    # Eliminar todos los datos de la sesión
    request.session.flush()
    # Redirigir a la página de inicio de sesión
    return redirect('Home') 