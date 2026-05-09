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
        fields = ['foto', 'telefono', 'direccion', 'fecha_nacimiento', 'facebook', 'instagram']
        widgets = {
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu número de contacto'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu dirección'}),
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'foto': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://facebook.com/tu-perfil'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://instagram.com/tu-perfil'}),
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


class AdminUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nueva contrasena'})
    )
    telefono = forms.CharField(max_length=20, required=True)
    direccion = forms.CharField(max_length=255, required=False)
    fecha_nacimiento = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    facebook = forms.URLField(required=False)
    instagram = forms.URLField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'telefono',
            'direccion',
            'fecha_nacimiento',
            'facebook',
            'instagram',
        ]

    def __init__(self, *args, **kwargs):
        self.perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)

        placeholders = {
            'username': 'Nombre de usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'correo@ejemplo.com',
            'telefono': 'Numero de contacto',
            'direccion': 'Direccion opcional',
            'facebook': 'https://facebook.com/usuario',
            'instagram': 'https://instagram.com/usuario',
        }

        for field_name in ['username', 'first_name', 'last_name', 'email', 'telefono', 'direccion', 'fecha_nacimiento', 'facebook', 'instagram']:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholders.get(field_name, '')
            })

        for field_name in ['is_active', 'is_staff', 'is_superuser']:
            self.fields[field_name].widget.attrs.update({'class': 'form-check-input'})

        self.fields['email'].required = True
        self.fields['is_active'].initial = True

        if self.perfil:
            self.fields['telefono'].initial = self.perfil.telefono
            self.fields['direccion'].initial = self.perfil.direccion
            self.fields['fecha_nacimiento'].initial = self.perfil.fecha_nacimiento
            self.fields['facebook'].initial = self.perfil.facebook
            self.fields['instagram'].initial = self.perfil.instagram

    def clean_username(self):
        username = self.cleaned_data['username']
        existe = User.objects.filter(username__iexact=username)

        if self.instance.pk:
            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():
            raise forms.ValidationError('Ya existe un usuario con ese nombre.')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        existe = User.objects.filter(email__iexact=email)

        if self.instance.pk:
            existe = existe.exclude(pk=self.instance.pk)

        if existe.exists():
            raise forms.ValidationError('Ya existe una cuenta registrada con ese correo.')

        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not self.instance.pk and not password:
            raise forms.ValidationError('La contrasena es obligatoria para usuarios nuevos.')

        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')

        if password:
            user.set_password(password)

        if commit:
            user.save()
            perfil, _ = ClientePerfil.objects.get_or_create(
                user=user,
                defaults={'telefono': '', 'direccion': ''}
            )
            perfil.telefono = self.cleaned_data['telefono']
            perfil.direccion = self.cleaned_data.get('direccion', '')
            perfil.fecha_nacimiento = self.cleaned_data.get('fecha_nacimiento')
            perfil.facebook = self.cleaned_data.get('facebook', '')
            perfil.instagram = self.cleaned_data.get('instagram', '')
            perfil.save()

        return user
