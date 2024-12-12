from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'contrasena', 'fecha_registro', 'fecha_nacimiento', 'telefono', 'curp', 'rfc', 'nacionalidad', 'genero')
    search_fields = ('nombre', 'apellido_paterno', 'apellido_materno', 'email', 'curp', 'rfc')
    list_filter = ('fecha_registro', 'nacionalidad', 'genero')
    ordering = ('-fecha_registro',)
    list_display_links = ('nombre', 'email')
    readonly_fields = ('fecha_registro',)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields  # No contrasena como readonly
        return self.readonly_fields