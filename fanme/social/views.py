from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
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
            evento = form.save(commit=False)
            try:
                request.user.eventos
            except Eventos.DoesNotExist:
                eventos = Eventos()
                eventos.creador = request.user
                eventos.save()
            creador = request.user.eventos
            evento.creador = creador
            evento.fecha_creacion = datetime.now()
            evento.save()
            form.save_m2m()
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
    if request.method == "POST":
        form = EventoForm(request.POST)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
        if form.is_valid():
            evento = form.save(commit=False)
            try:
                request.user.eventos
            except Eventos.DoesNotExist:
                eventos = Eventos()
                eventos.creador = request.user
                eventos.save()
            creador = request.user.eventos
            evento.creador = creador
            evento.fecha_creacion = datetime.now()
            evento.save()
            form.save_m2m()
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
def new_message(request):
    searchbox = SearchBox()
    messages = []
    if request.method == 'POST':
        form_new_message = MessageForm(request.POST)
        if form_new_message.is_valid():
            user_to_id = form_new_message.cleaned_data['user_to_id']
            mensaje = form_new_message.cleaned_data['mensaje']
            message = Mensaje()
            message.user_from_id = request.user.id
            message.user_to_id = user_to_id
            message.mensaje = mensaje
            message.fecha = datetime.datetime.now()
            message.save()
            messages.append("Se envio correctamente el mensaje")
            users = User()
            form_new_message = MessageForm()
        else:
            users = User.objects.all()
    else:
        form_new_message = MessageForm()
        users = User.objects.all()
    return render_to_response('social/new_message.html',
        {'form_new_message': form_new_message,
        'form_search': searchbox,
        'users': users,
        'messages': messages},
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
                mensajes_recibidos = request.user.mensajes_recibidos.filter(
                user_from__exact=user_id)
                mensajes_enviados = request.user.mensajes_enviados.filter(
                    user_to__exact=user_id)
                mensajes = sorted(chain(mensajes_enviados, mensajes_recibidos),
                    key=attrgetter('fecha'))
            else:
                mensajes_recibidos = request.user.mensajes_recibidos.filter(
                user_from__exact=user_id)
                mensajes_enviados = request.user.mensajes_enviados.filter(
                    user_to__exact=user_id)
                mensajes = sorted(chain(mensajes_enviados, mensajes_recibidos),
                    key=attrgetter('fecha'))
        else:
            mensajes_recibidos = request.user.mensajes_recibidos.filter(
                user_from__exact=user_id)
            mensajes_enviados = request.user.mensajes_enviados.filter(
                user_to__exact=user_id)
            mensajes = sorted(chain(mensajes_enviados, mensajes_recibidos),
                key=attrgetter('fecha'))
            form_response_message = MessageResponseForm()
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/messages_user.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes},
        context_instance=RequestContext(request))
