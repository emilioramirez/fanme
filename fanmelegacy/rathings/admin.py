from django.contrib import admin
from rathings.models import Like, Dislike
from rathings.custom_filter import is_item_or_comment
from django.contrib.admin import DateFieldListFilter


class LikeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('user', 'date_created', 'content_type')


class DislikeAdmin(admin.ModelAdmin):
    date_hierarchy = 'date_created'
    list_display = ('user', 'date_created', 'content_type')
    list_filter = (is_item_or_comment, ('date_created', DateFieldListFilter),)


admin.site.register(Like, LikeAdmin)
admin.site.register(Dislike, DislikeAdmin)
