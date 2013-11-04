from django.contrib import admin
from segmentation.models import Topico, Denuncia, AccionAnalisisDenuncia
from segmentation.models import EstadoAnalisisDenuncia, AnalisisDenuncia


class TopicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'padre')
    list_per_page = 50
    ordering = ('nombre',)
    search_fields = ['nombre', 'padre__nombre']

class AnalisisDenunciaAdmin(admin.ModelAdmin):
    list_display = ('fecha_creacion', 'fecha_resolucion', 'moderador',
        'descripcion', 'accion_tomada', 'estado', 'content_type', 'object_id',
        'content_object')


admin.site.register(Topico, TopicoAdmin)
admin.site.register(Denuncia)
admin.site.register(AccionAnalisisDenuncia)
admin.site.register(EstadoAnalisisDenuncia)
admin.site.register(AnalisisDenuncia, AnalisisDenunciaAdmin)
