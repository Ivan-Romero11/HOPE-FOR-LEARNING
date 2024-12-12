from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import make_password
from .models import Usuario, Becario, Domicilio, InformacionAcademica, EstudioSocioeconomico, EstadosBeca, InformacionBeca, DocumentosAcademicos, EstatusDocumentacion
from Convocatorias.models import Convocatoria
from django.urls import reverse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.utils import timezone
import mimetypes  # Alternativa para validar archivos
from Voluntarios.models import Programa,Inscripcion
from django.contrib import messages  # Para mostrar mensajes

# Decorador para deshabilitar la caché
def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

# Vista para mostrar el formulario
def formulario(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)  # Asegúrate de que el modelo es el correcto
    return render(request, "Becarios/registro_becario.html", {'convocatoria': convocatoria})

def registro_becario(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        email_usuario = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido_paterno = request.POST.get('apellido_paterno')
        apellido_materno = request.POST.get('apellido_materno')
        contrasena = request.POST.get('contrasena')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        telefono = request.POST.get('telefono')
        curp = request.POST.get('curp')
        genero = request.POST.get('genero')
        direccion = request.POST.get('direccion')
        ciudad = request.POST.get('ciudad')
        estado = request.POST.get('estado')
        codigo_postal = request.POST.get('codigo_postal')
        pais = request.POST.get('pais')  # Obtener el país
        nivel_academico = request.POST.get('nivel_academico')
        institucion_educativa = request.POST.get('institucion')
        carrera = request.POST.get('carrera')
        promedio = request.POST.get('promedio')
        fecha_ingreso = request.POST.get('fecha_ingreso')
        fecha_egreso = request.POST.get('fecha_egreso')
        ingreso_mensual = request.POST.get('ingreso_mensual')
        numero_dependientes = request.POST.get('numero_dependientes')
        vivienda = request.POST.get('vivienda')
        ocupacion_padres = request.POST.get('ocupacion_padres')
        nivel_educativo_padres = request.POST.get('nivel_educativo_padres')
        comentarios = request.POST.get('comentarios')

        # Obtener el nombre de la convocatoria
        nombre_convocatoria = request.POST.get('convocatoria')
        convocatoria = get_object_or_404(Convocatoria, nombre=nombre_convocatoria)

        # Manejar la subida de la foto
        foto = request.FILES.get('foto')

        try:
            # Comprobar si el usuario ya existe
            if Usuario.objects.filter(email=email_usuario).exists():
                  return JsonResponse({'success': False, 'message': 'El correo electrónico ya está registrado.'})
            # Crear el usuario
            usuario = Usuario(
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                email=email_usuario,
                contrasena=contrasena,
                fecha_nacimiento=fecha_nacimiento,
                telefono=telefono,
                curp=curp,
                genero=genero,
                foto=foto  # Guardar la foto subida
            )
            usuario.save()

            # Crear el becario asociado al usuario y asignar la convocatoria
            becario = Becario(usuario=usuario, convocatoria=convocatoria)
            becario.save()

            # Crear el domicilio con el nuevo campo "pais"
            domicilio = Domicilio(
                becario=becario,
                direccion=direccion,
                ciudad=ciudad,
                estado=estado,
                codigo_postal=codigo_postal,
                pais=pais  # Guardar el país
            )
            domicilio.save()

            # Crear la información académica
            info_academica = InformacionAcademica(
                becario=becario,
                nivel_academico=nivel_academico,
                institucion_educativa=institucion_educativa,
                carrera=carrera,
                promedio=promedio,
                fecha_ingreso=fecha_ingreso,
                fecha_egreso=fecha_egreso
            )
            info_academica.save()

            # Crear el estudio socioeconómico
            estudio_socioeconomico = EstudioSocioeconomico(
                becario=becario,
                ingreso_mensual=ingreso_mensual,
                numero_dependientes=numero_dependientes,
                vivienda=vivienda,
                ocupacion_padres=ocupacion_padres,
                nivel_educativo_padres=nivel_educativo_padres,
                comentarios=comentarios
            )
            estudio_socioeconomico.save()

            # Crear el estado de beca con estado "seleccionado"
            estado_beca = EstadosBeca(
                becario=becario,
                estado='seleccionado',
                comentarios='Estado inicial asignado.'
            )
            estado_beca.save()

            # Redirigir a la página principal
            return redirect('Home')  # Asegúrate de que 'home' esté configurado correctamente en tus urls.py

        except Exception as e:
            # En caso de error, mostrar el mensaje de error
            return HttpResponse(f"<h1>Error: {str(e)}</h1>")

    return HttpResponse("<h1>Esta vista solo acepta solicitudes POST.</h1>")
    
@no_cache
def base(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro2'))

    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuario, id=usuario_id)
    becario = get_object_or_404(Becario, usuario=usuario)

    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        constancia = request.FILES.get('constancia')
        boleta = request.FILES.get('boleta')
        promedio_general = request.POST.get('promedio_general')
        promedio_semestre = request.POST.get('promedio_semestre')

        # Validar que todos los campos estén completos
        if not (constancia and boleta and promedio_general and promedio_semestre):
            return JsonResponse({'success': False, 'message': 'Todos los campos son obligatorios. Por favor, completa todos los campos.'}, status=400)

        try:
            promedio_general = float(promedio_general)
            promedio_semestre = float(promedio_semestre)

            # Validar archivos cargados (solo PDF usando mimetypes)
            if mimetypes.guess_type(constancia.name)[0] != 'application/pdf':
                return JsonResponse({'success': False, 'message': 'La constancia debe ser un archivo PDF válido.'}, status=400)

            if mimetypes.guess_type(boleta.name)[0] != 'application/pdf':
                return JsonResponse({'success': False, 'message': 'La boleta debe ser un archivo PDF válido.'}, status=400)

            # Manejo de Documentos Académicos
            documentos, created = DocumentosAcademicos.objects.get_or_create(becario=becario)
            documentos.constancia = constancia
            documentos.boleta = boleta
            documentos.promedio_general = promedio_general
            documentos.promedio_semestre = promedio_semestre
            documentos.save()

            # Manejo del Estatus de Documentación
            estatus, created = EstatusDocumentacion.objects.get_or_create(documentos_academicos=documentos)
            estatus.estatus_constancia = "pendiente"
            estatus.estatus_boleta = "pendiente"
            estatus.comentarios_constancia = "Constancia cargada, en revisión."
            estatus.comentarios_boleta = "Boleta cargada, en revisión."
            estatus.fecha_revision = timezone.now()
            estatus.save()

            return JsonResponse({'success': True, 'message': 'Documentos guardados exitosamente y estatus actualizado.'})
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Error: Algunos valores ingresados no son válidos.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error al guardar documentos: {str(e)}'}, status=500)

    return render(request, "Becarios/principal.html", {'usuario': usuario, 'becario': becario})


@no_cache
def seccdatos(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro2'))

    # Obtener el ID del usuario de la sesión
    usuario_id = request.session['usuario_id']
    
    # Obtener el usuario activo
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Obtener el becario asociado al usuario
    becario = get_object_or_404(Becario, usuario=usuario)

    # Cargar los datos relacionados
    try:
        domicilio = get_object_or_404(Domicilio, becario=becario)
        info_academica = get_object_or_404(InformacionAcademica, becario=becario)
        informacion_beca = get_object_or_404(InformacionBeca, becario=becario)  # Cambiado para asegurar que se obtenga información
        estados_beca = EstadosBeca.objects.filter(becario=becario).first()  # Solo tomar el primer estado, ajusta según tu necesidad

        return render(request, "Becarios/seccdatos.html", {
            'usuario': usuario,
            'becario': becario,
            'domicilio': domicilio,
            'info_academica': info_academica,
            'informacion_beca': informacion_beca,
            'estados_beca': estados_beca
        })

    except Exception as e:
        return HttpResponse(f"<h1>Error al cargar los datos: {str(e)}</h1>")


@no_cache
def seccmibeca(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro2'))

    # Obtener el ID del usuario de la sesión
    usuario_id = request.session['usuario_id']
    
    # Obtener el usuario activo
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Obtener el becario asociado al usuario
    becario = get_object_or_404(Becario, usuario=usuario)

    # Obtener el estado de la beca (asumimos que existe un solo estado activo)
    estado_beca = EstadosBeca.objects.filter(becario=becario).first()  # Tomamos el primer estado
    
    # Pasar los datos a la plantilla
    return render(request, "Becarios/seccmibeca.html", {
        'usuario': usuario,
        'becario': becario,
        'estado_beca': estado_beca,
        'estatus_beca': estado_beca.estado if estado_beca else "Estado no disponible",  # Pasamos el estatus de la beca
        'grado_escolar': becario.informacionacademica.nivel_academico,  # Suponiendo que este campo existe
    })


@no_cache
def seccmiscali(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro2'))

    # Obtener el ID del usuario de la sesión
    usuario_id = request.session['usuario_id']
    
    # Obtener el usuario activo
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    # Obtener el becario asociado al usuario
    becario = get_object_or_404(Becario, usuario=usuario)
    
    # Obtener la información académica
    info_academica = get_object_or_404(InformacionAcademica, becario=becario)
    
    # Pasar los datos a la plantilla
    return render(request, "Becarios/seccmiscali.html", {
        'usuario': usuario,
        'becario': becario,
        'info_academica': info_academica
    })

@no_cache
def lista_programas(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro2'))

    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuario, id=usuario_id)
    becario = get_object_or_404(Becario, usuario=usuario)
    
    # Filtrar programas activos
    programas = Programa.objects.filter(estatus="Activo")  
    

    return render(request, 'Becarios/seccprogramas.html', {'programas': programas, 'usuario': usuario, 'becario': becario})


@no_cache
def inscribir_programa(request, programa_id):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro2'))

    usuario_id = request.session['usuario_id']
    usuario = get_object_or_404(Usuario, id=usuario_id)
    becario = get_object_or_404(Becario, usuario=usuario)
    programa = get_object_or_404(Programa, id=programa_id)

    # Crear la inscripción
    inscripcion = Inscripcion(becario=becario, programa=programa)
    inscripcion.save()

    # Incrementar el contador de becarios inscritos en el programa
    programa.becarios_inscritos += 1
    programa.save()

    # Añadir mensaje de éxito
    messages.success(request, f"Te has inscrito al programa '{programa.nombre_programa}' con éxito.")

    return redirect('lista_programas')  # Redirigir a la misma página de programas


