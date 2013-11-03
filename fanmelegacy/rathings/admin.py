from django.contrib import admin
from rathings.models import Like, Dislike


class LikeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('user', 'date_created', 'content_type')


class DislikeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('user', 'date_created', 'content_type')


admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)