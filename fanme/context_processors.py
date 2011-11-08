# -*- coding: utf-8 *-*
#from myproject.myapp.models import Foo


def indicadores(request):
    indicadores = {}
    try:
        rec = request.user.recomendaciones_recibidas.filter(
            estado='noleido').count()
        eventos = request.user.eventos_invitado.filter(estado="noleido").count()
        mensajes = request.user.mensajes_recibidos.filter(estado="noleido").count()
        notificaciones = request.user.notificaciones_recibidas.filter(
            estado="noleido").count()
        consultas = request.user.consultas_recibidas.filter(
            estado="noleido").count()
        indicadores['recomendaciones_noleidas'] = rec
        indicadores['eventos_nolidas'] = eventos
        indicadores['mensajes_nolidas'] = mensajes
        indicadores['notificaciones_noleidas'] = notificaciones
        indicadores['consultas_noleidas'] = consultas
    except:
        pass
    return indicadores
