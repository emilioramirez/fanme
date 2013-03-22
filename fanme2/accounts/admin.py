from django.contrib import admin
from accounts.models import ProfileUser


#class ProfileUserAdmin(admin.ModelAdmin):
    #list_display = ('__unicode__', 'fecha_nacimiento', 'sexo', 'is_first_time')
    #list_filter = ('sexo', 'is_first_time')
    #list_per_page = 50
    #ordering = ('user', 'fecha_nacimiento', 'sexo')
    #search_fields = ['user__first_name', 'user__last_name', 'user__email']


admin.site.register(ProfileUser)
