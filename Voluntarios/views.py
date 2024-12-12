from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Programa, Voluntario
from django.contrib import messages

# Decorador para deshabilitar la caché
def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper


@no_cache
def gestion_programas(request):
    if 'voluntario_id' not in request.session:
        return redirect('Registro5')  # Si no hay sesión activa, redirigir al formulario de login
    
    programas = Programa.objects.all()
    return render(request, 'Voluntarios/volunprogra.html', {'programas': programas})

# Decorador para deshabilitar la caché
def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper


@no_cache
def crear_programa(request):
    if request.method == 'POST':
        # Obtener el ID del voluntario desde la sesión
        voluntario_id = request.session.get('voluntario_id')
        if not voluntario_id:
            messages.error(request, 'Debes iniciar sesión para crear un programa.')
            return redirect('Registro5')  # Redirige al login si no hay sesión activa
        
        # Obtener el voluntario asociado
        try:
            voluntario = Voluntario.objects.get(id=voluntario_id)
        except Voluntario.DoesNotExist:
            messages.error(request, 'No se encontró un voluntario asociado.')
            return redirect('Registro5')
        
        # Obtener datos del formulario
        nombre_programa = request.POST.get('nombre_programa')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        estatus = request.POST.get('estatus')
        foto = request.FILES.get('imagen_programa')  # Obtener la imagen cargada

        # Validar el formato de la imagen
        if foto and not foto.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) :
            messages.error(request, 'Solo se permiten archivos de imagen (png, jpg, jpeg, gif).')
            return redirect('gestion_programas')

        # Crear el programa
        try:
            Programa.objects.create(
                nombre_programa=nombre_programa,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estatus=estatus,
                foto=foto,  # Asignar la foto cargada
                voluntario=voluntario,
            )
            messages.success(request, 'Programa creado exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al crear el programa: {e}')
        
        return redirect('gestion_programas')

    return render(request, 'Voluntarios/volunprogra.html')


def editar_programa(request, programa_id):
    programa = get_object_or_404(Programa, id=programa_id)
    
    if request.method == 'POST':
        # Actualizamos los campos de texto
        programa.nombre_programa = request.POST['nombre_programa']
        programa.descripcion = request.POST['descripcion']
        programa.fecha_inicio = request.POST['fecha_inicio']
        programa.fecha_fin = request.POST['fecha_fin']
        programa.estatus = request.POST['estatus']
        
        # Verificamos si se ha enviado un archivo de foto
        if 'foto' in request.FILES:
            programa.foto = request.FILES['foto']  # Actualiza la foto con la nueva imagen

        # Guardamos el objeto actualizado
        programa.save()
        
        # Mensaje de éxito
        messages.success(request, '¡Programa actualizado exitosamente!')
        
        return redirect('gestion_programas')
    
    return render(request, 'editar_programa.html', {'programa': programa})

# Eliminar un programa existente
def eliminar_programa(request, programa_id):
    programa = get_object_or_404(Programa, id=programa_id)
    if request.method == 'POST':
        programa.delete()
        messages.success(request, '¡Programa eliminado exitosamente!')
        return redirect('gestion_programas')