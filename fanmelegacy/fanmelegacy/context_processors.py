# -*- coding: utf-8 *-*
#from myproject.myapp.models import Foo
from django.db.models import Q
from dash.forms import SearchBox


def sidebar_indicators(request):
    context = {"form_search": SearchBox()}
    context['notificaciones_noleidas'] = request.user.notificaciones_recibidas.filter(~Q(estado='leido')).count()
    context['recomendaciones_noleidas'] = request.user.recomendaciones_recibidas.filter(estado='noleido').count()
    context['mensajes_nolidas'] = request.user.mensajes_recibidos.filter(estado='noleido').count()
    context['eventos_noleidos'] = request.user.invitacion_eventos.filter(estado='noleido').count()
    return context
