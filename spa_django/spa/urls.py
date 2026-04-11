from django.urls import path
from .views import (
    inicio,
    crear_cita,
    mis_citas,
    cancelar_cita,

    lista_servicios,
    crear_servicio,
    editar_servicio,
    eliminar_servicio,

    lista_empleados,
    crear_empleado,
    editar_empleado,
    eliminar_empleado,
)

urlpatterns = [
    path('', inicio, name='inicio'),
    path('cita/nueva/', crear_cita, name='crear_cita'),
    path('mis-citas/', mis_citas, name='mis_citas'),
    path('cita/cancelar/<int:cita_id>/', cancelar_cita, name='cancelar_cita'),

    path('admin-servicios/', lista_servicios, name='lista_servicios'),
    path('admin-servicios/nuevo/', crear_servicio, name='crear_servicio'),
    path('admin-servicios/editar/<int:servicio_id>/', editar_servicio, name='editar_servicio'),

    path('admin-servicios/eliminar/<int:servicio_id>/', eliminar_servicio, name='eliminar_servicio'),
    path('admin-empleados/', lista_empleados, name='lista_empleados'),
path('admin-empleados/nuevo/', crear_empleado, name='crear_empleado'),
path('admin-empleados/editar/<int:empleado_id>/', editar_empleado, name='editar_empleado'),
path('admin-empleados/eliminar/<int:empleado_id>/', eliminar_empleado, name='eliminar_empleado'),

    
]
