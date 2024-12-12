from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from Donantes.models import Donante, Donacion
from django.http import Http404
from django.template.loader import render_to_string
from xhtml2pdf import pisa


# Decorador para deshabilitar la caché
def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    return wrapper

# Vista para mostrar los datos del donante después del login
@no_cache
def base2(request):
    # Verificar si el donante tiene sesión activa
    if 'donante_id' not in request.session:
        return redirect('registro3')  # Si no hay sesión activa, redirigir al formulario de login
    
    donante_id = request.session['donante_id']
    
    try:
        donante = Donante.objects.get(id=donante_id)  # Obtener el donante por su ID desde la sesión
    except Donante.DoesNotExist:
        raise Http404("Donante no encontrado.")
    
    # Obtener todas las donaciones del donante
    donaciones = donante.donacion_set.all()

    # Renderizar la plantilla con los datos del donante
    return render(request, "Donantes/principal.html", {
        'donante': donante,
        'donaciones': donaciones
    })


@no_cache    
def reporte(request):
    # Verificar si el donante está autenticado en la sesión
    if 'donante_id' not in request.session:
        return redirect('registro3')  # Redirigir si no está autenticado
    
    # Obtener los datos del donante a partir del ID en la sesión
    donante_id = request.session['donante_id']
    donante = get_object_or_404(Donante, pk=donante_id)
    
    # Obtener las donaciones del donante
    donaciones = Donacion.objects.filter(donante=donante)
    
    # Renderizar la plantilla de reportes con los datos del donante y las donaciones
    return render(request, 'Donantes/reportes.html', {'donante': donante, 'donaciones': donaciones})


def reporte_pdf(request, donante_id):
    try:
        # Obtener el donante con el donante_id proporcionado
        donante = Donante.objects.get(id=donante_id)
    except Donante.DoesNotExist:
        return HttpResponse("Donante no encontrado.", status=404)
    
    # Obtener las donaciones del donante
    donaciones = Donacion.objects.filter(donante=donante)
    
    # Renderizar la plantilla con los datos del donante
    html = render_to_string('Donantes/reporte_pdf.html', {'donante': donante, 'donaciones': donaciones})

    # Crear una respuesta HTTP con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_donaciones.pdf"'

    # Convertir el HTML a PDF usando xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)

    # Verificar si hubo algún error
    if pisa_status.err:
        return HttpResponse("Error al generar el PDF", status=500)

    return response


@no_cache
def datos_donante(request, donante_id):
    # Obtener el donante por su ID
    donante = get_object_or_404(Donante, id=donante_id)
    
    # Renderizar la plantilla con los datos del donante
    return render(request, 'Donantes/datos_donante.html', {'donante': donante})