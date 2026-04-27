from django.contrib import admin
from .models import ClientePerfil


@admin.register(ClientePerfil)
class ClientePerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'direccion', 'fecha_nacimiento')
    search_fields = ('user__username', 'user__email', 'telefono')
