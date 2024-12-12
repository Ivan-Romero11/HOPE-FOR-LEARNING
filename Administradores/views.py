from datetime import date, timedelta
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from Becarios.models import Becario
from Coordinadores.models import Coordinador, Estado
from Donantes.models import Donacion
from django.db.models import Sum
from Convocatorias.models import Convocatoria, Estado
from Finanzas.models import Gasto, InformeTransparencia
from django.urls import reverse
from django.db import IntegrityError
from .models import Administrador

def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

@no_cache
def dashboard(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro4'))
    
    usuario_id = request.session['usuario_id']
    administrador = get_object_or_404(Administrador, usuario_id=usuario_id)

    total_becarios = Becario.objects.count()
    total_becarios_seleccionados = Becario.objects.filter(estadosbeca__estado='seleccionado').count()
    total_becarios_aceptados = Becario.objects.filter(estadosbeca__estado='aceptado').count()
    total_becarios_rechazados = Becario.objects.filter(estadosbeca__estado='rechazado').count()

    total_donaciones = Donacion.objects.aggregate(Sum('monto'))['monto__sum']
    total_donaciones = total_donaciones if total_donaciones else 0

    administradores = Administrador.objects.order_by('?')[:4]

    return render(request, 'administradores/dashboard.html', {
        'total_becarios_seleccionados': total_becarios_seleccionados,
        'total_becarios_aceptados': total_becarios_aceptados,
        'total_becarios_rechazados': total_becarios_rechazados,
        'total_becarios': total_becarios,
        'total_donaciones': total_donaciones,
        'administradores': administradores,
        'administrador': administrador,  # Pasa el administrador activo
    })


@no_cache
def lista_coordinadores(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro4'))
    
    usuario_id = request.session['usuario_id']
    administrador = get_object_or_404(Administrador, usuario_id=usuario_id)

    coordinadores = Coordinador.objects.filter(estado__estado='activo').select_related('usuario')
    return render(request, 'administradores/lista_coordinadores.html', {
        'coordinadores': coordinadores,
        'administrador': administrador,  # Pasa el administrador activo
    })


def agregar_convocatoria(request):
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
            messages.success(request, "Convocatoria agregada exitosamente.")
            return redirect('ver_convocatorias')
        except IntegrityError:
            messages.error(request, "El nombre de la convocatoria ya existe. Por favor, elige otro nombre.")
            return redirect('agregar_convocatoria')

    return render(request, 'lista_convocatorias_admi')

@no_cache
def ver_convocatorias(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro4'))
    
    usuario_id = request.session['usuario_id']
    administrador = get_object_or_404(Administrador, usuario_id=usuario_id)

    convocatorias = Convocatoria.objects.all()
    
    for convocatoria in convocatorias:
        if convocatoria.fecha_resultados:
            dias_restantes = (convocatoria.fecha_resultados - date.today()).days
            convocatoria.dias_restantes = max(dias_restantes, 0)
        else:
            convocatoria.dias_restantes = None

    return render(request, 'administradores/ver_convocatorias.html', {
        'convocatorias': convocatorias,
        'administrador': administrador,  # Pasa el administrador activo
    })


def editar_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)
    
    if request.method == 'POST':
        # Actualizar campos de la convocatoria con datos del formulario
        convocatoria.nombre = request.POST.get('nombre')
        convocatoria.comentario = request.POST.get('comentario')
        convocatoria.fecha_apertura = request.POST.get('fecha_apertura')
        convocatoria.fecha_limite_inscripcion = request.POST.get('fecha_limite_inscripcion')
        convocatoria.fecha_resultados = request.POST.get('fecha_resultados')
        convocatoria.estado = request.POST.get('estado')
        
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
    
def borrar_convocatoria(request, id):
    convocatoria = get_object_or_404(Convocatoria, id=id)  # Asegúrate de obtener la convocatoria correctamente
    if request.method == 'POST':
        convocatoria.delete()  # Elimina la convocatoria
        # Redirige a la lista de convocatorias con un mensaje de éxito
        return redirect(f"{reverse('ver_convocatorias')}?mensaje=Convocatoria eliminada exitosamente")
    convocatoria = get_object_or_404(Convocatoria, id=id)  # Asegúrate de obtener la convocatoria correctamente
    if request.method == 'POST':
        convocatoria.delete()  # Elimina la convocatoria
        return redirect('lista_convocatorias_admi')  # Redirige a la lista de convocatorias

    return render(request, 'Administradores/borrar_convocatoria_confirm.html', {'convocatoria': convocatoria})  # Muestra un confirmación

@no_cache
def lista_coordinadores_inactivos(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro4'))
    
    usuario_id = request.session['usuario_id']
    administrador = get_object_or_404(Administrador, usuario_id=usuario_id)
    
    # Obtener coordinadores
    coordinadores = Coordinador.objects.filter(estado__estado='inactivo').select_related('usuario')
    return render(request, 'administradores/lista_coordinadores_inactivos.html', {'coordinadores': coordinadores, 'administrador': administrador,})

@no_cache
def finanzas(request):
    if 'usuario_id' not in request.session:
        return redirect(reverse('Registro4'))
    
    usuario_id = request.session['usuario_id']
    administrador = get_object_or_404(Administrador, usuario_id=usuario_id)

    gastos = Gasto.objects.all()
    categorias = [g.categoria_gasto for g in gastos]
    montos = [float(g.monto) for g in gastos]

    informes = InformeTransparencia.objects.all()
    fechas = [inf.fecha_generacion.strftime("%Y-%m-%d") for inf in informes]
    saldos = [float(inf.saldo_final) for inf in informes]
    ultimo_informe = informes.order_by('-fecha_generacion').first()

    context = {
        'categorias': categorias,
        'montos': montos,
        'fechas': fechas,
        'saldos': saldos,
        'ultimo_informe': ultimo_informe,
        'administrador': administrador,  # Pasa el administrador activo
    }

    return render(request, 'administradores/finanzas.html', context)


def cerrar_sesion(request):
    request.session.flush()  # Elimina todos los datos de sesión
    return redirect('Home')  # Redirige a la página de inicio o cualquier otra página