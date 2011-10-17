from django.shortcuts import render_to_response
from fanme.dash.forms import SearchBox
from django.template import RequestContext
from fanme.social.forms import EventoForm
from fanme.social.models import Eventos, Evento
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


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
