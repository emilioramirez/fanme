from django.contrib import admin
from segmentation.models import Topico, Tag, Credibilidad, Denuncia


class TopicoAdmin(admin.ModelAdmin):
#    date_hierarchy = 'fecha_nacimiento'
#    fields =
#    filter_horizontal = ('items', 'following')
    list_display = ('nombre', 'padre')
#    list_filter = ()
    list_per_page = 50
    ordering = ('nombre',)
    search_fields = ['nombre', 'padre__nombre']


admin.site.register(Topico, TopicoAdmin)
admin.site.register(Tag)
admin.site.register(Credibilidad)
admin.site.register(Denuncia)
