from datetime import date

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CitaForm
from .models import Cita, Empleado, Servicio


def inicio(request):
    servicios_destacados = Servicio.objects.filter(activo=True).order_by('nombre')[:3]
    return render(request, 'spa/inicio.html', {'servicios_destacados': servicios_destacados})


def servicios_publicos(request):
    servicios = Servicio.objects.filter(activo=True).order_by('nombre')
    return render(request, 'spa/servicios_publicos.html', {'servicios': servicios})


@login_required
def crear_cita(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.cliente = request.user
            cita.save()

            messages.success(
                request,
                "Tu cita fue registrada correctamente."
            )
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

        messages.warning(
            request,
            "La cita fue cancelada correctamente."
        )

    return redirect('mis_citas')


@staff_member_required
def dashboard_admin(request):
    hoy = date.today()

    total_servicios = Servicio.objects.count()
    total_empleados = Empleado.objects.count()
    total_citas = Cita.objects.count()
    citas_hoy = Cita.objects.filter(fecha=hoy).count()

    citas_pendientes = Cita.objects.filter(estado='pendiente').count()
    citas_confirmadas = Cita.objects.filter(estado='confirmada').count()
    citas_completadas = Cita.objects.filter(estado='completada').count()
    citas_canceladas = Cita.objects.filter(estado='cancelada').count()

    ultimas_citas = Cita.objects.select_related(
        'cliente', 'servicio', 'empleado'
    ).order_by('-fecha', '-hora')[:5]

    context = {
        'total_servicios': total_servicios,
        'total_empleados': total_empleados,
        'total_citas': total_citas,
        'citas_hoy': citas_hoy,
        'citas_pendientes': citas_pendientes,
        'citas_confirmadas': citas_confirmadas,
        'citas_completadas': citas_completadas,
        'citas_canceladas': citas_canceladas,
        'ultimas_citas': ultimas_citas,
    }

    return render(request, 'spa/admin/dashboard.html', context)


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
        activo = request.POST.get('activo') == 'on'

        Servicio.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            duracion_minutos=duracion_minutos,
            precio=precio,
            activo=activo
        )

        messages.success(
            request,
            "Servicio creado correctamente."
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
        servicio.activo = request.POST.get('activo') == 'on'
        servicio.save()

        messages.success(
            request,
            "Servicio actualizado correctamente."
        )
        return redirect('lista_servicios')

    return render(request, 'spa/admin/servicio_form.html', {'servicio': servicio})


@staff_member_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        servicio.delete()

        messages.error(
            request,
            "Servicio eliminado correctamente."
        )
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
        activo = request.POST.get('activo') == 'on'

        Empleado.objects.create(
            nombre=nombre,
            especialidad=especialidad,
            activo=activo
        )

        messages.success(
            request,
            "Empleado creado correctamente."
        )
        return redirect('lista_empleados')

    return render(request, 'spa/admin/empleado_form.html')


@staff_member_required
def editar_empleado(request, empleado_id):
    empleado = get_object_or_404(Empleado, id=empleado_id)

    if request.method == 'POST':
        empleado.nombre = request.POST.get('nombre')
        empleado.especialidad = request.POST.get('especialidad')
        empleado.activo = request.POST.get('activo') == 'on'
        empleado.save()

        messages.success(
            request,
            "Empleado actualizado correctamente."
        )
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
        if tiene_citas_activas:
            messages.warning(
                request,
                "No puedes eliminar este empleado porque tiene citas activas."
            )
        else:
            empleado.delete()
            messages.error(
                request,
                "Empleado eliminado correctamente."
            )

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
    citas = Cita.objects.select_related(
        'cliente', 'servicio', 'empleado'
    ).order_by('-fecha', '-hora')
    return render(request, 'spa/admin/citas_lista.html', {'citas': citas})


@staff_member_required
def cambiar_estado_cita(request, cita_id, nuevo_estado):
    cita = get_object_or_404(Cita, id=cita_id)

    estados_validos = ['pendiente', 'confirmada', 'completada', 'cancelada']

    if nuevo_estado in estados_validos:
        cita.estado = nuevo_estado
        cita.save()

        messages.success(
            request,
            "Estado de la cita actualizado correctamente."
        )

    return redirect('lista_citas_admin')


@staff_member_required
def eliminar_cita_admin(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        cita.delete()

        messages.error(
            request,
            "Cita eliminada correctamente."
        )
        return redirect('lista_citas_admin')

    return render(request, 'spa/admin/cita_confirmar_eliminar.html', {'cita': cita})
