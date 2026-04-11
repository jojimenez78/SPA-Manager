from django import forms
from .models import Cita


class CitaForm(forms.ModelForm):

    class Meta:
        model = Cita
        fields = ['servicio', 'empleado', 'fecha', 'hora', 'notas']