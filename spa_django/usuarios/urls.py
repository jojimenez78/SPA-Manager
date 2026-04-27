from django.urls import path
from .views import perfil, registro

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('perfil/', perfil, name='perfil'),
]
