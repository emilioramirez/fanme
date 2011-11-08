from django.contrib import admin
from fanme.social.models import Evento, Notificacion, Mensaje, TipoEvento, Consulta


class EventoAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha_creacion'
#    fields =
    filter_horizontal = ('invitados',)
    list_display = ('nombre', 'fecha_creacion', 'fecha_inicio', 'fecha_fin',
        'localizacion', 'creador', 'estado')
    list_filter = ('estado', 'tipo')
    list_per_page = 50
    ordering = ('-fecha_creacion', '-fecha_inicio', 'nombre')
    search_fields = ['nombre', 'descripcion', 'creador__first_name',
        'creador__last_name', 'creador__email']


class MensajeAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
#    fields =
#    filter_horizontal = ('items', 'following')
    list_display = ('user_to', 'user_from', 'estado')
    list_filter = ('estado',)
    list_per_page = 50
    ordering = ('-fecha',)
    search_fields = ['user_to__first_name', 'user_to__last_name',
        'user_to__email', 'user_from__first_name', 'user_from__last_name',
        'user_from__email']


admin.site.register(Evento, EventoAdmin)
admin.site.register(Notificacion)
admin.site.register(Mensaje)
admin.site.register(Consulta)
