from django.contrib import admin
from core.models import Rubro, Pais, Provincia, Localidad, Topico
from core.models import Localizacion, TipoNotificacion, Notificacion


admin.site.register(Rubro)
admin.site.register(Pais)
admin.site.register(Provincia)
admin.site.register(Localidad)
admin.site.register(Localizacion)
admin.site.register(TipoNotificacion)
admin.site.register(Notificacion)
admin.site.register(Topico)
