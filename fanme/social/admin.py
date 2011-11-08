from django.contrib import admin
from fanme.social.models import Evento, Notificacion, Mensaje, Consulta

admin.site.register(Evento)
admin.site.register(Notificacion)
admin.site.register(Mensaje)
admin.site.register(Consulta)
