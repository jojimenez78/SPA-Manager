from django.contrib import admin
from .models import Servicio, Empleado, Cita


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio', 'duracion_minutos', 'activo')
    search_fields = ('nombre',)
    list_filter = ('activo',)


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especialidad', 'telefono', 'activo')
    search_fields = ('nombre', 'especialidad')
    list_filter = ('activo',)


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'servicio', 'empleado', 'fecha', 'hora', 'estado')
    search_fields = ('cliente__username', 'servicio__nombre', 'empleado__nombre')
    list_filter = ('estado', 'fecha')