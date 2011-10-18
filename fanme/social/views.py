from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from fanme.support.models import TipoNotificacion
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fanme.social.forms import MessageForm, MessageResponseForm
from fanme.dash.forms import SearchBox
from fanme.accounts.models import Persona
from fanme.social.models import Mensaje
from itertools import chain
from operator import attrgetter
import datetime

from fanme.social.forms import EventoForm
from fanme.social.models import Eventos, Evento
from fanme.support.models import Notificacion


@login_required(login_url='/accounts/user/')
def eventos(request):
    searchbox = SearchBox()
    try:
        eventos_creados = request.user.eventos.evento_set.all()
    except Eventos.DoesNotExist:
        eventos_creados = []
    try:
        eventos_invitado = request.user.evento_set.all()
    except Eventos.DoesNotExist:
        eventos_invitado = []
    temp = RequestContext(request, {'eventos_creados': eventos_creados,
        'eventos_invitado': eventos_invitado, 'form_search': searchbox})
    return render_to_response('social/eventos.html', temp)


@login_required(login_url='/accounts/user/')
def new_evento(request):
    searchbox = SearchBox()
    if request.method == "POST":
        form = EventoForm(request.POST)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
        if form.is_valid():
            usuarios = form.cleaned_data['invitados']
            evento = form.save(commit=False)
            try:
                request.user.eventos
            except Eventos.DoesNotExist:
                eventos = Eventos()
                eventos.creador = request.user
                eventos.save()
            creador = request.user.eventos
            evento.creador = creador
            evento.fecha_creacion = datetime.datetime.now()
            evento.save()
            form.save_m2m()
            enviar_notificaciones(usuarios,
                 "<a href='/dash/logbook/{0}'>{1}</a> ha creado un evento y te ha invitado".format(request.user.id, request.user.first_name+" "+request.user.last_name),
                 "/social/evento/{0}".format(evento.id),
                 "Evento",
                 "Te han invitado a un evento!")

            return HttpResponseRedirect('/social/eventos/')
    else:
        form = EventoForm()
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
    template_vars = RequestContext(request, {"form": form,
        'form_search': searchbox})
    return render_to_response('social/new_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def evento(request, evento_id):
    searchbox = SearchBox()
    try:
        evento = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        evento = []
    temp = RequestContext(request, {'form_search': searchbox, 'evento': evento})
    return render_to_response('social/evento.html', temp)


@login_required(login_url='/accounts/user/')
def edit_evento(request, evento_id):
    searchbox = SearchBox()
    try:
        evento_db = Evento.objects.get(id=evento_id)
    except Evento.DoesNotExist:
        return HttpResponseRedirect('/social/eventos/')
    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
        if form.is_valid():
            usuarios = form.cleaned_data['invitados']
            evento = form.save(commit=False)
            try:
                request.user.eventos
            except Eventos.DoesNotExist:
                eventos = Eventos()
                eventos.creador = request.user
                eventos.save()
#            creador = request.user.eventos
#            evento.creador = creador
#            evento.fecha_creacion = datetime.now()
            evento.save()
            form.save_m2m()
            enviar_notificaciones(usuarios,
                 "<a href='/dash/logbook/{0}'>{1}</a> ha creado un evento y te ha invitado".format(request.user.id, request.user.first_name+" "+request.user.last_name),
                 "/social/evento/{0}".format(evento.id),
                 "Evento",
                 "Te han invitado a un evento!")
            return HttpResponseRedirect('/social/eventos/')
    else:
        form = EventoForm(instance=evento_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
    template_vars = RequestContext(request, {"form": form, "user": request.user,
        'form_search': searchbox, 'evento': evento_db})
    return render_to_response('social/edit_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def delete_evento(request, evento_id):
    searchbox = SearchBox()
    try:
        evento_db = Evento.objects.get(id=evento_id)
        evento_db.delete()
        return HttpResponseRedirect('/social/eventos/')
    except Evento.DoesNotExist:
        return HttpResponseRedirect('/social/eventos/')
    template_vars = RequestContext(request, {
        'form_search': searchbox, 'evento': evento_db})
    return render_to_response('social/edit_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def messages(request):
    searchbox = SearchBox()
    try:
        mensajes_recibidos = request.user.mensajes_recibidos.all().values(
            'user_from').distinct()
        usuarios = []
        for dict in mensajes_recibidos.all():
            usuarios.append(User.objects.get(id=dict['user_from']))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/messages.html', {'form_search': searchbox,
        'mensajes_recibidos': usuarios},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def new_message(request):
    searchbox = SearchBox()
    if request.method == 'POST':
        form_new_message = MessageForm(request.POST)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form_new_message.fields["user_to_id"].queryset = users
        if form_new_message.is_valid():
            user_to_id = form_new_message.cleaned_data['user_to_id'].id
            mensaje = form_new_message.cleaned_data['mensaje']
            message = Mensaje()
            message.user_from_id = request.user.id
            message.user_to_id = user_to_id
            message.mensaje = mensaje
            message.fecha = datetime.datetime.now()
            message.save()
            return HttpResponseRedirect('/social/messages/')
    else:
        form_new_message = MessageForm()
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form_new_message.fields["user_to_id"].queryset = users
    return render_to_response('social/new_message.html',
        {'form_new_message': form_new_message,
        'form_search': searchbox},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def messages_user(request, user_id):
    searchbox = SearchBox()
    try:
        if request.method == 'POST':
            form_response_message = MessageResponseForm(request.POST)
            if form_response_message.is_valid():
                mensaje = form_response_message.cleaned_data['mensaje']
                message = Mensaje()
                message.user_from_id = request.user.id
                message.user_to_id = user_id
                message.mensaje = mensaje
                message.fecha = datetime.datetime.now()
                message.save()
                form_response_message = MessageResponseForm()
                mensajes = getMensajes(request, user_id)
            else:
                mensajes = getMensajes(request, user_id)
        else:
            mensajes = getMensajes(request, user_id)
            form_response_message = MessageResponseForm()
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/messages_user.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes},
        context_instance=RequestContext(request))


def getMensajes(request, user_id):
    mensajes_recibidos = request.user.mensajes_recibidos.filter(
        user_from__exact=user_id)
    mensajes_enviados = request.user.mensajes_enviados.filter(
        user_to__exact=user_id)
    mensajes = sorted(chain(mensajes_enviados, mensajes_recibidos),
        key=attrgetter('fecha'))
    return mensajes


@login_required(login_url='/accounts/user/')
def enterprise_query(request, user_id):
    searchbox = SearchBox()
    try:
        if request.method == 'POST':
            form_response_message = MessageResponseForm(request.POST)
            if form_response_message.is_valid():
                mensaje = form_response_message.cleaned_data['mensaje']
                message = Mensaje()
                message.user_from_id = request.user.id
                message.user_to_id = user_id
                message.mensaje = mensaje
                message.fecha = datetime.datetime.now()
                message.save()
                form_response_message = MessageResponseForm()
                mensajes = getMensajes(request, user_id)
            else:
                mensajes = getMensajes(request, user_id)
        else:
            mensajes = getMensajes(request, user_id)
            form_response_message = MessageResponseForm()
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/messages_user.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes},
        context_instance=RequestContext(request))


def enviar_notificaciones(usuarios, descripcion, url, tipo, resumen):
    for user in usuarios:
        notificacion = Notificacion()
        notificacion.usuario = user
        notificacion.descripcion = descripcion
        notificacion.url = url
        try:
            notificacion.tipo = TipoNotificacion.objects.get(nombre=tipo)
        except TipoNotificacion.DoesNotExist:
            tipo = TipoNotificacion()
            tipo.nombre = tipo
            tipo.descripcion = "tipo {0}".format(tipo)
            tipo.save()
            notificacion.tipo = tipo
        notificacion.leido = False
        notificacion.resumen = resumen
        notificacion.save()


@login_required(login_url='/accounts/user/')
def notificaciones(request):
    searchbox = SearchBox()
    try:
        notificaciones_leidas = request.user.notificacion_set.filter(leido=True)
    except Notificacion.DoesNotExist:
        notificaciones_leidas = []
    try:
        notificaciones_nuevas = request.user.notificacion_set.filter(leido=False)
        for notificacion in notificaciones_nuevas:
            notificacion.leido = True
            notificacion.save()
    except Notificacion.DoesNotExist:
        notificaciones_nuevas = []
    temp = RequestContext(request, {'notificaciones_nuevas': notificaciones_nuevas,
        'notificaciones_leidas': notificaciones_leidas, 'form_search': searchbox})
    return render_to_response('social/notificaciones.html', temp)


@login_required(login_url='/accounts/user/')
def delete_notificacion(request, notificacion_id):
    #searchbox = SearchBox()
    try:
        notificacion_db = Notificacion.objects.get(id=notificacion_id)
        notificacion_db.delete()
        return HttpResponseRedirect('/social/notificaciones/')
    except Notificacion.DoesNotExist:
        return HttpResponseRedirect('/social/notificaciones/')
    return HttpResponseRedirect('/social/notificaciones/')
