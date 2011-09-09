from django.contrib import admin
from fanme.support.models import Rubro, Topico, Item, Pais
from fanme.support.models import Provincia, Localidad, Marca, Localizacion


admin.site.register(Rubro)
admin.site.register(Topico)
admin.site.register(Item)

admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Marca)
admin.site.register(Localizacion)
