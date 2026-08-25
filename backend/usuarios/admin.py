from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import PermissaoExtra, Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ("username", "nome", "email", "perfil", "is_active")
    list_filter = ("perfil", "is_active")

    fieldsets = UserAdmin.fieldsets + (
    ("Dados do sistema de estoque", {
        "fields": ("nome", "perfil"),
    }),
)

@admin.register(PermissaoExtra)
class PermissaoExtraAdmin(admin.ModelAdmin):
    list_display = ("codigo",)