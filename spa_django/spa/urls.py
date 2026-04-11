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
]