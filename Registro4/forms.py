from django import forms
from Usuarios.models import Usuario

class LoginForm(forms.Form):
    email = forms.EmailField(label="Correo Electrónico", max_length=100)
    contrasena = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
