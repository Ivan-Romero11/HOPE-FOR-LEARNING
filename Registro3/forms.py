from django import forms
from Donantes.models import Donante

class LoginForm(forms.ModelForm):
    class Meta:
        model = Donante
        fields = ['nombre', 'email']  # Solo incluimos los campos 'nombre' y 'email'
        labels = {
            'nombre': 'Nombre',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'max_length': 100}),
        }
