from django.contrib import admin
from accounts.models import Persona, Empresa


class PersonaAdmin(admin.ModelAdmin):
    date_hierarchy = 'fecha_nacimiento'
#    fields =
    filter_horizontal = ('items', 'following')
    list_display = ('__unicode__', 'fecha_nacimiento', 'sexo', 'is_first_time')
    list_filter = ('sexo', 'is_first_time')
    list_per_page = 50
    ordering = ('user', 'fecha_nacimiento', 'sexo')
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


class EmpresaAdmin(admin.ModelAdmin):
    filter_horizontal = ('rubros',)
    list_display = ('__unicode__', 'razon_social', 'is_first_time')
    list_filter = ('is_first_time',)
    list_per_page = 50
    ordering = ('user', 'razon_social')
    search_fields = ['user__first_name', 'user__last_name', 'user__email']


admin.site.register(Persona, PersonaAdmin)
admin.site.register(Empresa, EmpresaAdmin)
