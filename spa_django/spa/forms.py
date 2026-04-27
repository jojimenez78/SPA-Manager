from datetime import date, time

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
        widgets = {
            'notas': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Cuéntanos si deseas agregar una preferencia o comentario para tu cita.'
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['servicio'].queryset = Servicio.objects.filter(activo=True)
        self.fields['empleado'].queryset = Empleado.objects.filter(activo=True)
        self.fields['servicio'].empty_label = 'Selecciona un servicio'
        self.fields['empleado'].empty_label = 'Selecciona un especialista'
        self.fields['fecha'].widget.attrs.update({'class': 'form-control', 'min': date.today().isoformat()})
        self.fields['hora'].widget.attrs.update({'class': 'form-control'})
        self.fields['servicio'].widget.attrs.update({'class': 'form-select'})
        self.fields['empleado'].widget.attrs.update({'class': 'form-select'})
        self.fields['notas'].widget.attrs.update({'class': 'form-control'})

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')

        if fecha and fecha < date.today():
            raise forms.ValidationError("No puedes reservar citas en fechas pasadas.")

        return fecha

    def clean_hora(self):
        hora = self.cleaned_data.get('hora')

        if hora and (hora < time(8, 0) or hora > time(18, 0)):
            raise forms.ValidationError("El horario permitido es de 8:00 AM a 6:00 PM.")

        return hora

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
            )

            if self.instance.pk:
                existe = existe.exclude(pk=self.instance.pk)

            if existe.exists():
                raise forms.ValidationError(
                    'Ese empleado ya tiene una cita reservada en esa fecha y hora.'
                )

        return cleaned_data
