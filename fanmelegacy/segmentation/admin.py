from django.contrib import admin
from segmentation.models import Topico, Denuncia, AccionAnalisisDenuncia
from segmentation.models import EstadoAnalisisDenuncia, AnalisisDenuncia
from django.contrib.admin import DateFieldListFilter


class TopicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'padre')
    list_per_page = 50
    ordering = ('nombre',)
    search_fields = ['nombre', 'padre__nombre']

class AnalisisDenunciaAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha_creacion'
    list_display = ('fecha_creacion', 'fecha_resolucion', 'moderador',
        'descripcion', 'estado', 'content_type', 'object_id')
    search_fields = ['moderador__first_name', 'moderador__last_name', 'moderador__email']
    list_filter = (('fecha_creacion', DateFieldListFilter),
        ('fecha_resolucion', DateFieldListFilter), 'estado',)


admin.site.register(Topico, TopicoAdmin)
admin.site.register(Denuncia)
admin.site.register(AccionAnalisisDenuncia)
admin.site.register(EstadoAnalisisDenuncia)
admin.site.register(AnalisisDenuncia, AnalisisDenunciaAdmin)
