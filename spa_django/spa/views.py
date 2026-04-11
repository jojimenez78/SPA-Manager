from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CitaForm
from .models import Cita

def inicio(request):
    return render(request, 'spa/inicio.html')

@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = request.user
            cita.save()
            return redirect('mis_citas')
    else:
        form = CitaForm()

    return render(request, 'spa/crear_cita.html', {'form': form})

@login_required
def mis_citas(request):
    citas = Cita.objects.filter(cliente=request.user).order_by('-fecha', '-hora')
    return render(request, 'spa/mis_citas.html', {'citas': citas})