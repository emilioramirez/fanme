from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType


class is_item_or_comment(admin.SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('Objeto denunciado')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'content_type__id__exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        modelo_item = ContentType.objects.get(app_label="items", model="item")
        modelo_comentario = ContentType.objects.get(app_label="comments", model="comment")
        return (
            (modelo_item.id, _('items')),
            (modelo_comentario.id, _('comentarios')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value():
            return queryset.filter(content_type__id__exact=self.value())
