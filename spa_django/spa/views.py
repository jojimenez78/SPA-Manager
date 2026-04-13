from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from .forms import CitaForm
from .models import Cita, Servicio, Empleado


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


@login_required
def cancelar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, cliente=request.user)

    if cita.estado in ['pendiente', 'confirmada']:
        cita.estado = 'cancelada'
        cita.save()

    return redirect('mis_citas')


@staff_member_required
def lista_servicios(request):
    servicios = Servicio.objects.all().order_by('nombre')
    return render(request, 'spa/admin/servicios_lista.html', {'servicios': servicios})


@staff_member_required
def crear_servicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        duracion_minutos = request.POST.get('duracion_minutos')
        precio = request.POST.get('precio')
        activo = True if request.POST.get('activo') == 'on' else False

        Servicio.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            duracion_minutos=duracion_minutos,
            precio=precio,
            activo=activo
        )
        return redirect('lista_servicios')

    return render(request, 'spa/admin/servicio_form.html')


@staff_member_required
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre')
        servicio.descripcion = request.POST.get('descripcion')
        servicio.duracion_minutos = request.POST.get('duracion_minutos')
        servicio.precio = request.POST.get('precio')
        servicio.activo = True if request.POST.get('activo') == 'on' else False
        servicio.save()
        return redirect('lista_servicios')

    return render(request, 'spa/admin/servicio_form.html', {'servicio': servicio})


@staff_member_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        servicio.delete()
        return redirect('lista_servicios')

    return render(request, 'spa/admin/servicio_confirmar_eliminar.html', {'servicio': servicio})


@staff_member_required
def lista_empleados(request):
    empleados = Empleado.objects.all().order_by('nombre')
    return render(request, 'spa/admin/empleados_lista.html', {'empleados': empleados})


@staff_member_required
def crear_empleado(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        especialidad = request.POST.get('especialidad')
        activo = True if request.POST.get('activo') == 'on' else False

        Empleado.objects.create(
            nombre=nombre,
            especialidad=especialidad,
            activo=activo
        )

        return redirect('lista_empleados')

    return render(request, 'spa/admin/empleado_form.html')


@staff_member_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.especialidad = request.POST.get('especialidad')
        empleado.activo = True if request.POST.get('activo') == 'on' else False
        empleado.save()

        return redirect('lista_empleados')

    return render(request, 'spa/admin/empleado_form.html', {'empleado': empleado})


@staff_member_required
def eliminar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    tiene_citas_activas = Cita.objects.filter(
        empleado=empleado,
        estado__in=['pendiente', 'confirmada']
    ).exists()

    if request.method == 'POST':
        if not tiene_citas_activas:
            empleado.delete()
        return redirect('lista_empleados')

    return render(
        request,
        'spa/admin/empleado_confirmar_eliminar.html',
        {
            'empleado': empleado,
            'tiene_citas_activas': tiene_citas_activas
        }
    )


@staff_member_required
def lista_citas_admin(request):
    citas = Cita.objects.all().order_by('-fecha', '-hora')
    return render(request, 'spa/admin/citas_lista.html', {'citas': citas})


@staff_member_required
def cambiar_estado_cita(request, cita_id, nuevo_estado):
    cita = get_object_or_404(Cita, id=cita_id)

    estados_validos = ['pendiente', 'confirmada', 'completada', 'cancelada']

    if nuevo_estado in estados_validos:
        cita.estado = nuevo_estado
        cita.save()

    return redirect('lista_citas_admin')


@staff_member_required
def eliminar_cita_admin(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        cita.delete()
        return redirect('lista_citas_admin')

    return render(request, 'spa/admin/cita_confirmar_eliminar.html', {'cita': cita})