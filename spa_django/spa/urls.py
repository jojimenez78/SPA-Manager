from django.urls import path
from .views import inicio, crear_cita, mis_citas

urlpatterns = [
    path('', inicio, name='inicio'),
    path('cita/nueva/', crear_cita, name='crear_cita'),
    path('mis-citas/', mis_citas, name='mis_citas'),
]