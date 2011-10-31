from django.contrib import admin
from fanme.segmentation.models import Topico, Tag, Credibilidad, Denuncia

admin.site.register(Topico)
admin.site.register(Tag)
admin.site.register(Credibilidad)
admin.site.register(Denuncia)

