from django import forms
from .models import Cita, Servicio, Empleado


class CitaForm(forms.ModelForm):
    fecha = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    hora = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    class Meta:
        model = Cita
        fields = ['servicio', 'empleado', 'fecha', 'hora', 'notas']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        self.fields['empleado'].queryset = Empleado.objects.filter(activo=True)

    def clean(self):
        cleaned_data = super().clean()
        empleado = cleaned_data.get('empleado')
        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        if empleado and fecha and hora:
            existe = Cita.objects.filter(
                empleado=empleado,
                fecha=fecha,
                hora=hora,
                estado__in=['pendiente', 'confirmada']
            ).exists()

            if existe:
                raise forms.ValidationError(
                    'Ese empleado ya tiene una cita reservada en esa fecha y hora.'
                )

        return cleaned_data