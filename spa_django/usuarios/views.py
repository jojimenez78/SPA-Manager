from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .forms import RegistroUsuarioForm, UsuarioPerfilForm
from .models import ClientePerfil


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu cuenta fue creada correctamente. Ya puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def perfil(request):
    perfil_usuario, _ = ClientePerfil.objects.get_or_create(
        user=request.user,
        defaults={'telefono': '', 'direccion': ''}
    )

    if request.method == 'POST':
        form = UsuarioPerfilForm(request.POST, request.FILES, instance=perfil_usuario, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil fue actualizado correctamente.')
            return redirect('perfil')
    else:
        form = UsuarioPerfilForm(instance=perfil_usuario, user=request.user)

    return render(
        request,
        'usuarios/perfil.html',
        {
            'form': form,
            'perfil_usuario': perfil_usuario,
        }
    )


@require_POST
def logout_view(request):
    logout(request)
    return render(request, 'registration/logged_out.html')
