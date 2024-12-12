from django import forms
from .models import Coordinador

class CoordinadorForm(forms.ModelForm):
    class Meta:
        model = Coordinador
        fields = ['usuario', 'departamento']
