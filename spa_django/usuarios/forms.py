from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ClientePerfil


class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)
    telefono = forms.CharField(max_length=20)
    direccion = forms.CharField(max_length=255, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'telefono', 'direccion', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widgets = {
            'username': {'placeholder': 'Tu nombre de usuario'},
            'email': {'placeholder': 'correo@ejemplo.com'},
            'telefono': {'placeholder': 'Tu número de contacto'},
            'direccion': {'placeholder': 'Dirección opcional'},
            'password1': {'placeholder': 'Crea una contraseña segura'},
            'password2': {'placeholder': 'Repite la contraseña'},
        }

        for field_name, attrs in widgets.items():
            self.fields[field_name].widget.attrs.update({'class': 'form-control', **attrs})

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Ya existe una cuenta registrada con este correo electrónico.')

        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            ClientePerfil.objects.create(
                user=user,
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion']
            )

        return user


class UsuarioPerfilForm(forms.ModelForm):
    first_name = forms.CharField(required=False, label='Nombre')
    last_name = forms.CharField(required=False, label='Apellido')
    email = forms.EmailField(required=True, label='Correo electrónico')

    class Meta:
        model = ClientePerfil
        fields = ['foto', 'telefono', 'direccion', 'fecha_nacimiento']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de contacto'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu dirección'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['first_name'].initial = self.user.first_name
        self.fields['last_name'].initial = self.user.last_name
        self.fields['email'].initial = self.user.email

        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tu nombre'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Tu apellido'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'correo@ejemplo.com'})

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Ese correo electrónico ya está siendo usado por otra cuenta.')

        return email

    def save(self, commit=True):
        perfil = super().save(commit=False)
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.email = self.cleaned_data['email']

        if commit:
            self.user.save()
            perfil.user = self.user
            perfil.save()

        return perfil
