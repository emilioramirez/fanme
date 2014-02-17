from django.contrib import admin
from support.models import Rubro, Pais, Provincia, Localidad
from support.models import Localizacion, TipoNotificacion, Notificacion


admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(TipoNotificacion)
admin.site.register(Notificacion)
