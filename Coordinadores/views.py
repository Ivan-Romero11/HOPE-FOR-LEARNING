from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Becarios.models import Becario, EstadosBeca
from Convocatorias.models import Convocatoria, Estado
from Donantes.models import Donacion
from django.db.models import Sum
from .models import Coordinador
from Voluntarios.models import Voluntario, Estado, Programa
from datetime import date, timedelta
from .models import Coordinador
from .forms import CoordinadorForm
from Finanzas.models import Gasto, InformeTransparencia
from Becarios.models import Becario, InformacionBeca, InformacionAcademica, DocumentosAcademicos, EstatusDocumentacion
from django.urls import reverse
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.utils.timezone import now

def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

@no_cache
def voluntarios(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    # Obtener voluntarios cuyo estado es "seleccionado" en la relación con Estado
    voluntarios = Voluntario.objects.filter(estado__estado='seleccionado').select_related('usuario')
    
    return render(request, 'coordinadores/voluntarios.html', {'voluntarios': voluntarios, 'coordinador': coordinador})

@no_cache
def voluntarios_aceptados(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    # Obtener voluntarios cuyo estado es "aceptado" en la relación con Estado
    voluntarios = Voluntario.objects.filter(estado__estado='aceptado').select_related('usuario')
    
    return render(request, 'coordinadores/voluntarios_aceptados.html', {'voluntarios': voluntarios, 'coordinador': coordinador})

@no_cache
def voluntarios_rechazados(request):
    
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    # Obtener voluntarios cuyo estado es "rechazado" en la relación con Estado
    voluntarios = Voluntario.objects.filter(estado__estado='rechazado').select_related('usuario')
    
    return render(request, 'coordinadores/voluntarios_rechazados.html', {'voluntarios': voluntarios, 'coordinador': coordinador})

def actualizar_estado_voluntario(request):
    if request.method == 'POST':
        voluntario_id = request.POST.get('voluntario_id')
        estado = request.POST.get('estado')
        comentarios = request.POST.get('motivo')

        # Verificar si el campo comentarios está vacío, y asignar un valor por defecto si es necesario
        if not comentarios:
            comentarios = 'Sin comentarios'  # Valor por defecto si no se proporciona comentario

        # Obtén el voluntario y su estado actual
        voluntario = get_object_or_404(Voluntario, id=voluntario_id)
        estado_obj = get_object_or_404(Estado, voluntario=voluntario)  # Obtener el estado existente

        # Actualizar el estado y comentarios del voluntario
        estado_obj.estado = estado
        estado_obj.comentarios = comentarios
        estado_obj.save()  # Guardar los cambios

        # Redirigir a la lista de voluntarios
        return redirect('voluntarios')  # Aquí 'voluntarios' es el nombre de la URL que lista los voluntarios
@no_cache
def finanzas(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    # Obtener los gastos para crear la gráfica
    gastos = Gasto.objects.all()
    categorias = [g.categoria_gasto for g in gastos]
    montos = [float(g.monto) for g in gastos]

    # Obtener los informes de transparencia
    informes = InformeTransparencia.objects.all()
    fechas = [inf.fecha_generacion.strftime("%Y-%m-%d") for inf in informes]
    saldos = [float(inf.saldo_final) for inf in informes]

    # Obtener el informe más reciente
    ultimo_informe = informes.order_by('-fecha_generacion').first()

    context = {
        'categorias': categorias,
        'montos': montos,
        'fechas': fechas,
        'saldos': saldos,
        'ultimo_informe': ultimo_informe,
    }
    return render(request, 'administradores/finanzas.html', context, {'coordinador': coordinador})

@no_cache
def lista_becariosacep(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    # Obtener becarios con el estado "aceptado" y sus datos relacionados
    becarios = Becario.objects.filter(estadosbeca__estado='aceptado').select_related('usuario')
    return render(request, 'coordinadores/becarios_aceptados.html', {'becarios': becarios, 'coordinador': coordinador})

@no_cache
def lista_becarios(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    becarios = Becario.objects.filter(estadosbeca__estado='seleccionado').select_related('usuario')
    return render(request, 'coordinadores/becarios.html', {'becarios': becarios, 'coordinador': coordinador})

@no_cache
def lista_becariosrecha(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    # Obtener becarios con el estado "rechazado" y sus datos relacionados
    becarios = Becario.objects.filter(estadosbeca__estado='rechazado').select_related('usuario')
    return render(request, 'coordinadores/becarios_rechazados.html', {'becarios': becarios, 'coordinador': coordinador})

def actualizar_estado_becario(request):
    if request.method == 'POST':
        becario_id = request.POST.get('becario_id')
        motivo = request.POST.get('motivo')
        estado = request.POST.get('estado')

        # Validar que se han proporcionado los datos necesarios
        if not becario_id or not motivo or not estado:
            messages.error(request, "ID del becario, motivo o estado no proporcionados.")
            return redirect('lista_becarios')

        # Obtener el becario o retornar 404 si no se encuentra
        becario = get_object_or_404(Becario, id=becario_id)
        
        # Generar comentarios a partir del motivo y el estado
        comentarios = f"Motivo: {motivo}. Estado actualizado a: {estado}."

        # Utilizar update_or_create para actualizar o crear un nuevo estado de beca
        EstadosBeca.objects.update_or_create(
            becario=becario,
            defaults={
                'estado': estado, 
                'comentarios': comentarios
            }
        )
         # Enviar correo al becario sobre su estado
        enviar_correo_becario(becario_id, estado, motivo)

        
        # Mensaje de éxito después de la actualización
        messages.success(request, f"Estado de beca actualizado para {becario.usuario.nombre}.")
        return redirect('lista_becarios')
    
    # Si no es POST, retorna una respuesta de método no permitido
    return HttpResponseBadRequest("Método de solicitud no permitido.")

def actualizar_estado_becario(request):
    if request.method == 'POST':
        becario_id = request.POST.get('becario_id')
        motivo = request.POST.get('motivo')
        estado = request.POST.get('estado')

        # Validar que se han proporcionado los datos necesarios
        if not becario_id or not motivo or not estado:
            messages.error(request, "ID del becario, motivo o estado no proporcionados.")
            return redirect('lista_becarios')

        # Obtener el becario o retornar 404 si no se encuentra
        becario = get_object_or_404(Becario, id=becario_id)
        
        # Generar comentarios a partir del motivo y el estado
        comentarios = f"Motivo: {motivo}. Estado actualizado a: {estado}."

        # Utilizar update_or_create para manejar el estado de beca
        EstadosBeca.objects.update_or_create(
            becario=becario,
            defaults={'comentarios': comentarios, 'estado': estado}
        )
        
        # Enviar correo al becario sobre su estado
        enviar_correo_becario(becario_id, estado, motivo)


        # Mensaje de éxito después de la actualización
        messages.success(request, f"Estado de beca actualizado para {becario.usuario.nombre}.")
        return redirect('lista_becarios')
    
    return HttpResponseBadRequest("Método de solicitud no permitido.")

@no_cache
def agregar_convocatoria(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        comentario = request.POST['comentario']
        fecha_apertura = request.POST['fecha_apertura']
        fecha_limite_inscripcion = request.POST['fecha_limite_inscripcion']
        fecha_resultados = request.POST['fecha_resultados']
        presupuesto_limite_becarios = request.POST['presupuesto_limite_becarios']
        monto_beca = request.POST['monto_beca']
        foto = request.FILES.get('foto')  # Retrieve uploaded image

        if float(monto_beca) != 0:
            cantidad_becarios = int(float(presupuesto_limite_becarios) / float(monto_beca))
        else:
            cantidad_becarios = 0

        nueva_convocatoria = Convocatoria(
            nombre=nombre,
            comentario=comentario,
            fecha_apertura=fecha_apertura,
            fecha_limite_inscripcion=fecha_limite_inscripcion,
            fecha_resultados=fecha_resultados,
            presupuesto_limite_becarios=presupuesto_limite_becarios,
            monto_beca=monto_beca,
            foto=foto,
            cantidad_becarios=cantidad_becarios
        )

        try:
            nueva_convocatoria.save()
            estado_inicial = Estado(convocatoria=nueva_convocatoria, estado='pendiente')
            estado_inicial.save()
            # Redirigir a la página con el mensaje en la URL
            success_url = f"{reverse('ver_convocatorias')}?mensaje=Convocatoria agregada exitosamente"
            return redirect(success_url)
        except IntegrityError:
            messages.error(request, "El nombre de la convocatoria ya existe. Por favor, elige otro nombre.")
            return redirect('agregar_convocatoria')

    return render(request, 'lista_convocatorias')


@no_cache
def lista_convocatorias(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    convocatorias = Convocatoria.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        comentario = request.POST.get('comentario')
        fecha_apertura = request.POST.get('fecha_apertura')
        fecha_limite_inscripcion = request.POST.get('fecha_limite_inscripcion')
        fecha_resultados = request.POST.get('fecha_resultados')
        
        # Obtener la duración del programa desde el formulario
        duracion_str = request.POST.get('duracion_programa')
        
        try:
            # Convertir el valor de la duración a un objeto timedelta
            duracion_programa = timedelta(days=int(duracion_str))
        except (ValueError, TypeError):
            duracion_programa = None

        # Obtener el archivo de la foto si fue subido
        foto = request.FILES.get('foto')

        nueva_convocatoria = Convocatoria(
            nombre=nombre,
            comentario=comentario,
            fecha_apertura=fecha_apertura,
            fecha_limite_inscripcion=fecha_limite_inscripcion,
            fecha_resultados=fecha_resultados,
            duracion_programa=duracion_programa,
            foto=foto  # Guardar la imagen en el campo foto
        )
        nueva_convocatoria.save()
        return redirect('lista_convocatorias')

    return render(request, 'Coordinadores/convocatorias.html', {'convocatorias': convocatorias, 'coordinador': coordinador})

@no_cache
def ver_convocatorias(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    convocatorias = Convocatoria.objects.all()
    
    for convocatoria in convocatorias:
        if convocatoria.fecha_resultados:
            dias_restantes = (convocatoria.fecha_resultados - date.today()).days
            convocatoria.dias_restantes = max(dias_restantes, 0)
        else:
            convocatoria.dias_restantes = None

    return render(request, 'Coordinadores/ver_convocatorias.html', {'convocatorias': convocatorias, 'coordinador': coordinador})

@no_cache
def editar_convocatoria(request, id):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    convocatoria = get_object_or_404(Convocatoria, id=id)
    
    if request.method == 'POST':
        # Actualizar campos de la convocatoria con datos del formulario
        convocatoria.nombre = request.POST.get('nombre')
        convocatoria.comentario = request.POST.get('comentario')
        convocatoria.fecha_apertura = request.POST.get('fecha_apertura')
        convocatoria.fecha_limite_inscripcion = request.POST.get('fecha_limite_inscripcion')
        convocatoria.fecha_resultados = request.POST.get('fecha_resultados')
        
        # Actualizar presupuesto y monto de beca
        convocatoria.presupuesto_limite_becarios = request.POST.get('presupuesto_limite_becarios')
        convocatoria.monto_beca = request.POST.get('monto_beca')
        
        # Calcular cantidad de becarios con base en presupuesto y monto de beca
        try:
            monto_beca = float(convocatoria.monto_beca) if convocatoria.monto_beca else 0
            presupuesto = float(convocatoria.presupuesto_limite_becarios) if convocatoria.presupuesto_limite_becarios else 0
            convocatoria.cantidad_becarios = int(presupuesto // monto_beca) if monto_beca > 0 else 0
        except ValueError:
            convocatoria.cantidad_becarios = 0
        
        # Verificar si se subió una nueva imagen; si no, mantener la imagen existente
        if 'foto' in request.FILES:
            convocatoria.foto = request.FILES['foto']
        
        convocatoria.save()  # Guardar los cambios
        
        # Redirigir con un mensaje de éxito
        return redirect(f"{reverse('ver_convocatorias')}?mensaje=Convocatoria actualizada exitosamente")
    
@no_cache
def borrar_convocatoria(request, id):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    convocatoria = get_object_or_404(Convocatoria, id=id)  # Asegúrate de obtener la convocatoria correctamente
    if request.method == 'POST':
        convocatoria.delete()  # Elimina la convocatoria
        # Redirige a la lista de convocatorias con un mensaje de éxito
        return redirect(f"{reverse('ver_convocatorias')}?mensaje=Convocatoria eliminada exitosamente")
    
@no_cache
def lista_coordinadores(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)    
    
    coordinadores = Coordinador.objects.all()
    return render(request, 'coordinadores/lista_becarios.html', {'coordinadores': coordinadores, 'coordinador': coordinador})

@no_cache
def editar_coordinador(request, pk):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    coordinador = get_object_or_404(Coordinador, pk=pk)
    if request.method == 'POST':
        form = CoordinadorForm(request.POST, instance=coordinador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coordinador actualizado correctamente.')
            return redirect('lista_coordinadores')  # Cambia a la URL que lista los coordinadores
    else:
        form = CoordinadorForm(instance=coordinador)
    
    return render(request, 'coordinadores/editar_coordinador.html', {'form': form, 'coordinador': coordinador})

@no_cache
def dashboard(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)    
    
     # Contar todos los becarios sin importar su estatus
    total_becarios = Becario.objects.count()  # Cuenta todos los becarios en la base de datos

    total_becarios_seleccionados = Becario.objects.filter(estadosbeca__estado='seleccionado').count()  # Cuenta solo los becarios seleccionados

    total_becarios_aceptados = Becario.objects.filter(estadosbeca__estado='aceptado').count()  # Cuenta solo los becarios aceptados

    total_becarios_rechazados = Becario.objects.filter(estadosbeca__estado='rechazado').count()  # Cuenta solo los becarios rechazados


    # Sumar todos los montos donados
    total_donaciones = Donacion.objects.aggregate(Sum('monto'))['monto__sum']  # Suma de los montos donados

    # Si no hay donaciones, establece total_donaciones a 0
    total_donaciones = total_donaciones if total_donaciones is not None else 0

    # Pasar los valores a la plantilla
    return render(request, 'coordinadores/lista_becarios.html', {
        'total_becarios_seleccionados': total_becarios_seleccionados,
        'total_becarios_aceptados': total_becarios_aceptados,
        'total_becarios_rechazados': total_becarios_rechazados,
        'total_becarios': total_becarios,
        'total_donaciones': total_donaciones,
        'coordinador': coordinador
        
    })

def dashboard_coordinadores(request):
    # Extraer datos para la gráfica
    total_becarios = Becario.objects.count()
    promedio_general = InformacionAcademica.objects.aggregate(Avg('promedio'))['promedio__avg'] # type: ignore
    becas_totales = InformacionBeca.objects.aggregate(Sum('monto_beca'))['monto_beca__sum']

    # Preparar los datos que se pasarán al contexto
    data_grafica = {
        'total_becarios': total_becarios,
        'promedio_general': promedio_general,
        'becas_totales': becas_totales,
    }
    
    return render(request, 'Coordinadores/dashboard.html', data_grafica)

def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de sesión
    return redirect('Home')  # Redirige a la página de inicio o cualquier otra página
def enviar_correo_becario(becario_id, estado, motivo):
    # Obtener el becario por su ID
    becario = get_object_or_404(Becario, id=becario_id)

    # Obtener la convocatoria asociada al becario
    convocatoria = becario.convocatoria if hasattr(becario, 'convocatoria') else None

    # Definir el asunto y el mensaje del correo
    if estado == 'aceptado':
        asunto = '¡Felicidades! Has sido aceptado'
        mensaje_html = render_to_string(
            'Coordinadores/emails/becario_aceptado.html',
            {'becario': becario, 'convocatoria': convocatoria, 'motivo': motivo}
        )
    else:
        asunto = 'Notificación de estado de beca'
        mensaje_html = render_to_string(
            'Coordinadores/emails/becario_rechazado.html',
            {'becario': becario, 'convocatoria': convocatoria, 'motivo': motivo}
        )

    mensaje_texto = strip_tags(mensaje_html)

    # Enviar el correo
    send_mail(
        asunto,
        mensaje_texto,
        'hopeforlearning53d@gmail.com',  # Remitente
        [becario.usuario.email],  # Destinatario
        html_message=mensaje_html,
        fail_silently=False,
    )

    
def validar_documentos(request):
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id) 
    
    # Filtrar los documentos que tienen al menos un documento (constancia o boleta) no aceptado
    documentos_pendientes = DocumentosAcademicos.objects.exclude(
        estatusdocumentacion__estatus_constancia='Aceptado', 
        estatusdocumentacion__estatus_boleta='Aceptado'
    )

    return render(request, 'Coordinadores/validaciondoc.html', {
        'documentos_pendientes': documentos_pendientes,
        'coordinador': coordinador
    })


def actualizar_estatus_documento(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        documento_id = request.POST.get('documento_id')  # ID del becario relacionado
        tipo_documento = request.POST.get('tipo_documento')
        accion = request.POST.get('accion')
        comentarios = request.POST.get('comentarios')

        try:
            # Obtener el documento académico usando el ID del becario
            documento = DocumentosAcademicos.objects.get(becario_id=documento_id)

            # Obtener el estatus de documentación relacionado con el documento
            estatus_documentacion = EstatusDocumentacion.objects.get(documentos_academicos=documento)

            # Actualizar el estado del documento según la acción seleccionada
            if accion == 'Aceptar':
                if tipo_documento == 'Constancia':
                    estatus_documentacion.estatus_constancia = 'Aceptado'
                elif tipo_documento == 'Boleta':
                    estatus_documentacion.estatus_boleta = 'Aceptado'
            elif accion == 'Rechazar':
                if tipo_documento == 'Constancia':
                    estatus_documentacion.estatus_constancia = 'Rechazado'
                elif tipo_documento == 'Boleta':
                    estatus_documentacion.estatus_boleta = 'Rechazado'

            # Guardar los comentarios si están presentes
            if tipo_documento == 'Constancia':
                estatus_documentacion.comentarios_constancia = comentarios
            elif tipo_documento == 'Boleta':
                estatus_documentacion.comentarios_boleta = comentarios

            # Guardar los cambios en el estatus
            estatus_documentacion.save()

            # Verificar si ambos documentos son aceptados
            if estatus_documentacion.estatus_constancia == 'Aceptado' and estatus_documentacion.estatus_boleta == 'Aceptado':
                # Obtener la información académica relacionada con el becario
                informacion_academica = InformacionAcademica.objects.get(becario_id=documento_id)

                # Incrementar el grado del becario
                if informacion_academica.grado is None:
                    informacion_academica.grado = 1  # Asignar un valor inicial si es None
                else:
                    # Asegurarse de que el grado sea un número entero
                    informacion_academica.grado = int(informacion_academica.grado) + 1  # Incrementar grado en 1

                # Guardar los cambios en la información académica (actualizar el grado)
                informacion_academica.save()

            # Mensaje de éxito
            messages.success(request, f"El documento de {documento.becario.usuario.nombre} ha sido {accion.lower()} correctamente.")

        except DocumentosAcademicos.DoesNotExist:
            messages.error(request, "El documento no existe o hubo un error al procesar la solicitud.")
            return redirect('validar_documentos')  # Redirigir si hay un error

        except EstatusDocumentacion.DoesNotExist:
            messages.error(request, "No se encontró el estatus de documentación.")
            return redirect('validar_documentos')  # Redirigir si hay un error

        except InformacionAcademica.DoesNotExist:
            messages.error(request, "No se encontró la información académica del becario.")
            return redirect('validar_documentos')  # Redirigir si hay un error

        return redirect('validar_documentos')  # Redirigir después de procesar la acción

    # Si no es un POST, simplemente redirigir
    return redirect('validar_documentos')

@no_cache
def programas(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro1'))
    
    usuario_id = request.session['usuario_id']
    coordinador = get_object_or_404(Coordinador, usuario_id=usuario_id)
    
    programas_pendientes = Programa.objects.filter(estatus='Pendiente')  # Filtra los programas con estatus 'pendiente'
    return render(request, 'Coordinadores/programas.html', {'programas': programas_pendientes, 'coordinador': coordinador})

def actualizar_estatus_programa(request):
    if request.method == 'POST':
        programa_id = request.POST.get('programa_id')
        accion = request.POST.get('accion_tipo')
        comentarios = request.POST.get('motivo', '')

        # Validar si existe el programa
        programa = get_object_or_404(Programa, id=programa_id)

        print(f"Acción recibida: {accion} para el programa {programa_id}")

        if accion == 'aprobar':
            programa.estatus = 'aprobado'
            mensaje = "El programa ha sido aprobado exitosamente."
        elif accion == 'rechazar':
            programa.estatus = 'rechazado'
            mensaje = "El programa ha sido rechazado."
        else:
            return JsonResponse({'error': 'Acción no válida.'}, status=400)

        # Guardar cambios en el programa
        programa.save()

        # Registrar el cambio de estado
        Estado.objects.create(
            voluntario=programa.voluntario,
            estado=programa.estatus,
            comentarios=comentarios,
            fecha_cambio=now()
        )

        print(f"Nuevo estatus: {programa.estatus}")

        # Redirigir al listado de programas
        return redirect('programas')

    return JsonResponse({'error': 'Método no permitido.'}, status=405)