from django.contrib import admin
from fanme.items.models import Item, Marca, Comentario, Recomendacion

admin.site.register(Item)
admin.site.register(Marca)
admin.site.register(Comentario)
admin.site.register(Recomendacion)
