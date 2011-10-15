from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from fanme.social.forms import MessageForm

from fanme.dash.forms import SearchBox
from fanme.accounts.models import Persona
from fanme.social.models import Mensaje
from itertools import chain
from operator import attrgetter
import datetime


@login_required(login_url='/accounts/user/')
def messages(request):
    searchbox = SearchBox()
    try:
        mensajes_recibidos = request.user.mensajes_recibidos.all().values(
            'user_from').distinct()
        usuarios = []
        for dict in mensajes_recibidos.all():
            usuarios.append(User.objects.get(id=dict['user_from']))
        for usuario in usuarios:
            print usuario.first_name
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/messages.html', {'form_search': searchbox,
        'mensajes_recibidos': usuarios},
        context_instance=RequestContext(request))


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
            message.fecha = datetime.date.today()
            message.save()
            messages.append("Se envio correctamente el mensaje")
            users = User()
            form_new_message = MessageForm()
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
#        if request.method == 'POST':
#        else:
            mensajes_recibidos = request.user.mensajes_recibidos.filter(
                user_from__exact=user_id)
            mensajes_enviados = request.user.mensajes_enviados.filter(
                user_to__exact=user_id)
            mensajes = sorted(chain(mensajes_enviados, mensajes_recibidos),
                key=attrgetter('fecha'))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/messages_user.html', {
        'form_search': searchbox,
        'mensajes': mensajes},
        context_instance=RequestContext(request))
