# finanzas/admin.py
from django.contrib import admin
from .models import Gasto, InformeTransparencia

@admin.register(Gasto)
class GastoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'monto', 'fecha_gasto', 'responsable', 'categoria_gasto')
    search_fields = ('descripcion', 'responsable__usuario__nombre')
    list_filter = ('fecha_gasto', 'categoria_gasto')

@admin.register(InformeTransparencia)
class InformeTransparenciaAdmin(admin.ModelAdmin):
    list_display = ('fecha_generacion', 'total_donaciones', 'total_gastos', 'saldo_final', 'responsable')
    search_fields = ('responsable__usuario__nombre',)
    list_filter = ('fecha_generacion',)