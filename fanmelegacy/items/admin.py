from django.contrib import admin
from items.models import Item, Marca, Comentario, Recomendacion
from items.models import ItemImagen


class ItemAdmin(admin.ModelAdmin):
#     date_hierarchy = 'fecha_nacimiento'
#    fields =
    filter_horizontal = ('users_are_comment',)
    list_display = ('nombre', 'topico', 'cantidad_fans',
        'cantidad_recomendaciones')
    list_filter = ('topico',)
    list_per_page = 50
    ordering = ('-cantidad_fans', 'nombre', 'topico')
    search_fields = ['nombre', 'topico__nombre', 'cantidad_fans', 'descripcion']


class ComentarioAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
#    fields =
#    filter_horizontal = ('users_are_comment',)
    list_display = ('user', 'item', 'me_gusta', 'denuncias')
    list_filter = ('fecha',)
    list_per_page = 50
    ordering = ('-denuncias', 'me_gusta', 'item', 'user')
    search_fields = ['user__first_name', 'user__last_name', 'user__email',
        'comentario']


class RecomendacionAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha'
#    fields =
#    filter_horizontal = ('users_are_comment',)
    list_display = ('user_origen', 'user_destino', 'item')
    list_filter = ('fecha', 'estado', 'item')
    list_per_page = 50
    ordering = ('-fecha', 'item')
    search_fields = ['user_destino__first_name', 'user_destino__last_name',
        'user_destino__email', 'user_origen__first_name',
        'user_origen__last_name', 'user_origen__email', 'item__nombre',
        'item__descripcion']


admin.site.register(Item, ItemAdmin)
admin.site.register(Marca)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Recomendacion, RecomendacionAdmin)
admin.site.register(ItemImagen)
