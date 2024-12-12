from django.shortcuts import render
from .models import Terminos  # Importar el modelo Terminos

def terminos(request):
    terminos = Terminos.objects.all()  # Obtener todos los términos
    return render(request, "Terminos/terminos.html", {'terminos': terminos})

