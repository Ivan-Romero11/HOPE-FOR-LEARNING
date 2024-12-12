from django.shortcuts import render

# Create your views here.
def blog(request):
    return render(request, "Blog/principal.html")

def seccion1(request):
    return render(request, "Blog/seccion1.html")

def seccion2(request):
    return render(request, "Blog/seccion2.html")

def seccion3(request):
    return render(request, "Blog/seccion3.html")

def seccion4(request):
    return render(request, "Blog/seccion4.html")

def seccion5(request):
    return render(request, "Blog/seccion5.html")

def seccion6(request):
    return render(request, "Blog/seccion6.html")

def seccion7(request):
    return render(request, "Blog/seccion7.html")

def seccion8(request):
    return render(request, "Blog/seccion8.html")

def seccion9(request):
    return render(request, "Blog/seccion9.html")

def seccion10(request):
    return render(request, "Blog/seccion10.html")

def seccion11(request):
    return render(request, "Blog/seccion11.html")

def seccion12(request):
    return render(request, "Blog/seccion12.html")

def aviso_privacidad(request):
    return render(request, 'Convocatorias/AvisodePrivacidad.html')