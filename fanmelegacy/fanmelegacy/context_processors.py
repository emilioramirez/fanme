# -*- coding: utf-8 *-*
#from myproject.myapp.models import Foo
from django.db.models import Q
from django.core.urlresolvers import reverse
from dash.forms import SearchBox
from segmentation.models import EstadoAnalisisDenuncia


def sidebar_indicators(request):
    context = {"form_search": SearchBox()}
    try:
        context['notificaciones_noleidas'] = request.user.notificaciones_recibidas.filter(~Q(estado='leido')).count()
        context['recomendaciones_noleidas'] = request.user.recomendaciones_recibidas.filter(estado='noleido').count()
        context['mensajes_nolidas'] = request.user.mensajes_recibidos.filter(estado='noleido').count()
        context['eventos_noleidos'] = request.user.invitacion_eventos.filter(estado='noleido').count()
        estado, creado = EstadoAnalisisDenuncia.objects.get_or_create(estado="creado")
        context['denuncias_creadas'] = request.user.analisisdenuncia_set.filter(estado=estado).count()
    except AttributeError:
        pass
    return context

def logo_url(request):
    context = {}
    if request.user.is_authenticated():
        context['logo_url'] = reverse('dashboard')
    return context