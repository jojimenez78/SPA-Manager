from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ClientePerfil


@admin.register(ClientePerfil)
class ClientePerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'telefono', 'direccion')
    search_fields = ('user__username', 'telefono')