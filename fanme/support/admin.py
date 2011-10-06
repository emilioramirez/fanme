from django.contrib import admin
from fanme.support.models import Rubro, Pais, Provincia, Localidad
from fanme.support.models import Localizacion


admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Localizacion)
