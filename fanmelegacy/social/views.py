# -*- encoding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from support.models import TipoNotificacion
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from social.forms import MessageForm, MessageResponseForm
from social.forms import MessageQueryForm
from dash.forms import SearchBox
from accounts.models import Persona, Empresa
from social.models import Mensaje
from itertools import chain
from operator import attrgetter
from datetime import datetime, date

from social.forms import EventoForm, NotificationForm
from social.models import Evento, Consulta, Notificacion
#from support.models import Notificacion
from items.models import Item
from django.db.models import Q


@login_required(login_url='/accounts/user/')
def eventos(request):
    searchbox = SearchBox()
    no_hay_eventos = True
    try:
        eventos_creados = request.user.eventos_creados.all().order_by(
            'fecha_inicio')
    except Evento.DoesNotExist:
        eventos_creados = []
    try:
        eventos_invitado = request.user.eventos_invitado.all().order_by(
            'fecha_inicio')
        eventos_noleidos = request.user.eventos_invitado.filter(
            estado="noleido")
        for evento in eventos_noleidos:
            evento.estado = "leido"
            evento.save()
        notificaciones_noleidas = get_cant_notificaciones(request)
    except Evento.DoesNotExist:
        eventos_invitado = []
    if eventos_creados or eventos_invitado:
        no_hay_eventos = False
    temp = RequestContext(request, {'eventos_creados': eventos_creados,
        'eventos_invitado': eventos_invitado, 'no_hay_eventos': no_hay_eventos,
        'form_search': searchbox, 'notificaciones_noleidas': notificaciones_noleidas})
    return render_to_response('social/eventos.html', temp)


@login_required(login_url='/accounts/user/')
def new_evento(request):
    searchbox = SearchBox()
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
        if form.is_valid():
            evento = form.save(commit=False)
            creador = request.user
            evento.creador = creador
            evento.fecha_creacion = datetime.now()
            try:
                evento.imagen = request.FILES['imagen']
            except KeyError:
                pass
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
    creador = False
    try:
        evento = Evento.objects.get(id=evento_id)
        if (evento.creador == request.user):
            creador = True
    except Evento.DoesNotExist:
        evento = []
    temp = RequestContext(request, {'form_search': searchbox, 'evento': evento,
        'creador': creador})
    return render_to_response('social/evento.html', temp)


@login_required(login_url='/accounts/user/')
def edit_evento(request, evento_id):
    searchbox = SearchBox()
    try:
        evento_db = Evento.objects.get(id=evento_id)
        if not (evento_db.creador == request.user):
            return HttpResponseRedirect('/social/eventos/')
    except Evento.DoesNotExist:
        return HttpResponseRedirect('/social/eventos/')
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES, instance=evento_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
        if form.is_valid():
            evento = form.save(commit=False)
            try:
                evento.imagen = request.FILES['imagen']
            except KeyError:
                pass
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
        if (evento_db.creador == request.user):
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
        msj_noleidos = request.user.mensajes_recibidos.filter(estado="noleido")
        for msj in msj_noleidos:
            msj.estado = "leido"
            msj.save()
        notificaciones_noleidas = get_cant_notificaciones(request)
    except Persona.DoesNotExist:  # Esto para que esta?
        return HttpResponseRedirect('/dash/empresa/')  # Esto para que esta?
    return render_to_response('social/messages.html', {'form_search': searchbox,
        'usuarios': usuarios, 'notificaciones_noleidas': notificaciones_noleidas},
        context_instance=RequestContext(request))


def get_cant_notificaciones(request):
    return request.user.notificaciones_recibidas.filter(
            estado='noleido').count()


@login_required(login_url='/accounts/user/')
def new_message(request):
    searchbox = SearchBox()
    messages=[]
    list_ids = request.user.followers.values_list('user', flat=True)
    users = User.objects.filter(id__in=list_ids)
    if request.method == 'POST':
        form_new_message = MessageForm(request.POST)
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
            messages.append("Tu mensaje ha sido enviado exitosamente")
            form_new_message = MessageForm()
            return HttpResponseRedirect('/social/new_message/')
    else:
        form_new_message = MessageForm()
#        list_ids = request.user.followers.values_list('user', flat=True)
#        users = User.objects.filter(id__in=list_ids)
        form_new_message.fields["user_to_id"].queryset = users
    return render_to_response('social/new_message.html',
        {'form_new_message': form_new_message,
        'form_search': searchbox,
        'messages': messages},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def messages_user(request, user_id):
    searchbox = SearchBox()
    try:  # porque esto?
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
    except Persona.DoesNotExist:  # porque esto?
        return HttpResponseRedirect('/dash/empresa/')  # porque esto?
    return render_to_response('social/messages_user.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes,
        'user_id': user_id},
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
def company_query(request, company_id):
    searchbox = SearchBox()
    messages = []
    no_posee_items = False
    if request.method == 'POST':
        form_query_message = MessageQueryForm(request.POST)
        if form_query_message.is_valid():
            mensaje_consulta = form_query_message.cleaned_data['consulta']
            item = form_query_message.cleaned_data['item']
            consulta = Consulta()
            consulta.item = item
            consulta.user_from = request.user
            consulta.user_to = User.objects.get(id__exact=company_id)
            consulta.mensaje = mensaje_consulta
            consulta.fecha = datetime.now()
            consulta.estado = "noleido"
            consulta.save()
            messages.append("Tu consulta ha sido enviada exitosamente")
            form_query_message = MessageQueryForm()
        else:
            items_plan = items_en_plan_vigente(company_id)
            if items_plan == None or items_plan.count() == 0:
                messages.append("La empresa no posee items registrados. No se le podrá enviar ninguna consulta.")
                no_posee_items = True
            form_query_message.fields["item"].queryset = items_plan
    else:
        form_query_message = MessageQueryForm()
        items_plan = items_en_plan_vigente(company_id)
        if items_plan == None or items_plan.count() == 0:
            messages.append("La empresa no posee items registrados. No se le podrá enviar ninguna consulta.")
            no_posee_items = True
        form_query_message.fields["item"].queryset = items_plan
    return render_to_response('social/consulta_a_empresa.html', {
        'form_search': searchbox,
        'company_id': company_id,
        'form_query_message': form_query_message,
        'no_posee_items': no_posee_items,
        'messages': messages},
        context_instance=RequestContext(request))


def items_en_plan_vigente(company_id):
    empresa = User.objects.get(pk=company_id)
    planes = empresa.plan_empresa.all().order_by('-fecha_fin_vigencia')
    items_plan = None
    if planes:
        plan = planes[0]
        if plan.fecha_fin_vigencia > date.today():
            items_plan = plan.item
    return items_plan


@login_required(login_url='/accounts/user/')
def ver_consultas(request):
    searchbox = SearchBox()
    consultas_recibidas = request.user.consultas_recibidas.all().values(
            'item').distinct()
    items = []
    consultas_noleidas = request.user.consultas_recibidas.filter(
        estado="noleido").count()
    for dict in consultas_recibidas.all():
        items.append(Item.objects.get(id=dict['item']))
    return render_to_response('social/ver_consultas.html', {
        'form_search': searchbox,
        'consultas_recibidas': items, 'consultas_noleidas': consultas_noleidas},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def ver_consultas_item(request, item_id):
    searchbox = SearchBox()
    item = Item.objects.get(id=item_id)
    items_consultas = item.mis_consultas.values(
        'user_from').distinct()
    users = []
    for dict in items_consultas.all():
        users.append(User.objects.get(id=dict['user_from']))
    consultas_noleidas = request.user.consultas_recibidas.filter(
        estado="noleido").count()
#    consultas = []
#    for usuario in users:
#        consultas = usuario.consultas_enviadas.all()
#    for consulta in consultas:
#        print consulta.item.id
#        print item_id
#        if consulta.item.id == item_id:
#            print "algo"
#        else:
#            print "choto"
    return render_to_response('social/ver_consultas_item.html', {
        'form_search': searchbox,
        'usuario_consulta_item': users,
        'item_id': item_id, 'consultas_noleidas': consultas_noleidas},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def ver_consultas_item_usuario(request, item_id, user_id):
    searchbox = SearchBox()
    user = User.objects.get(id=user_id)
    item_consultado = Item.objects.get(id=item_id)
    consulta_item = Consulta.objects.filter(
        Q(item=item_consultado), Q(user_from=user))
    for consulta in consulta_item.all():
        consulta.estado = "leido"
        consulta.save()
    consultas_noleidas = request.user.consultas_recibidas.filter(
        estado="noleido").count()
    return render_to_response('social/ver_consulta_item_usuario.html', {
        'form_search': searchbox,
        'usuario': user, 'consultas_noleidas': consultas_noleidas,
        'consulta_item': consulta_item},
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
        notificaciones_enviadas = request.user.notificaciones_enviadas.all()
        consultas_noleidas = request.user.consultas_recibidas.filter(
            estado="noleido").count()
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/notificaciones.html', {
        'form_search': searchbox, 'consultas_noleidas': consultas_noleidas,
        'notificaciones_enviadas': notificaciones_enviadas},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def notificacion(request, notificacion_id):
    searchbox = SearchBox()
    empresa = False
    try:
        notificacion = Notificacion.objects.get(id=notificacion_id)
        if (notificacion.empresa == request.user):
            empresa = True
    except Evento.DoesNotExist:
        notificacion = []
    temp = RequestContext(request, {'form_search': searchbox,
        'notificacion': notificacion,
        'empresa': empresa})
    return render_to_response('social/notificaciones.html', temp)


@login_required(login_url='/accounts/user/')
def edit_notificacion(request, notificacion_id):
    searchbox = SearchBox()
    try:
        notificacion_db = Notificacion.objects.get(id__exact=notificacion_id)
        if not (notificacion_db.empresa == request.user):
            return HttpResponseRedirect('/social/notificaciones/')
    except Evento.DoesNotExist:
        return HttpResponseRedirect('/social/notificaciones/')
    if request.method == "POST":
        form = NotificationForm(request.POST, instance=notificacion_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["usuarios_to"].queryset = users
        if form.is_valid():
            notificacion = form.save(commit=False)
            try:
                notificacion.imagen = request.FILES['imagen']
            except KeyError:
                pass
            notificacion.estado = 'actualizado'
            notificacion.save()
            form.save_m2m()
            return HttpResponseRedirect('/social/notificaciones/')
    else:
        form = NotificationForm(instance=notificacion_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["usuarios_to"].queryset = users
    template_vars = RequestContext(request, {"form": form, "user": request.user,
        'form_search': searchbox, 'notificacion': notificacion_db})
    return render_to_response('social/edit_notificacion.html', template_vars)


@login_required(login_url='/accounts/user/')
def delete_notificacion(request, notificacion_id):
    searchbox = SearchBox()
    try:
        notificacion_db = Notificacion.objects.get(id=notificacion_id)
        if (notificacion_db.empresa == request.user):
            notificacion_db.delete()
        return HttpResponseRedirect('/social/notificaciones/')
    except Notificacion.DoesNotExist:
        return HttpResponseRedirect('/social/notificaciones/')
    template_vars = RequestContext(request, {
        'form_search': searchbox, 'notificacion': notificacion_db})
    return HttpResponseRedirect('/social/edit_notificacion/', template_vars)


@login_required(login_url='/accounts/user/')
def company_messages(request):
    searchbox = SearchBox()
    try:
        mensajes_recibidos = request.user.mensajes_recibidos.all().values(
            'user_from').distinct()
        consultas_noleidas = request.user.consultas_recibidas.filter(
            estado="noleido").count()
        usuarios = []
        for dict in mensajes_recibidos.all():
            usuarios.append(User.objects.get(id=dict['user_from']))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/company_messages.html', {
        'form_search': searchbox, 'consultas_noleidas': consultas_noleidas,
        'mensajes_recibidos': usuarios},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def company_response_message(request, user_id):
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
    return render_to_response('social/company_response_message.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def new_notification(request):
    searchbox = SearchBox()
    if request.method == "POST":
        form = NotificationForm(request.POST)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["usuarios_to"].queryset = users
        if form.is_valid():
            notification = form.save(commit=False)
            notification.fecha_creacion = datetime.now()
            notification.empresa = request.user
            try:
                notification.imagen = request.FILES['imagen']
            except KeyError:
                pass
            notification.save()
            form.save_m2m()
            return HttpResponseRedirect('/social/notificaciones/')
    else:
        form = NotificationForm()
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["usuarios_to"].queryset = users
    template_vars = RequestContext(request, {"form": form,
        'form_search': searchbox})
    return render_to_response('social/new_notification.html', template_vars)


@login_required(login_url='/accounts/user/')
def user_main_view_notifications(request):
    searchbox = SearchBox()
    try:
        notificaciones_recibidas = request.user.notificaciones_recibidas.all(
            ).values('empresa').distinct()
        usuarios = []
        for dict in notificaciones_recibidas.all():
            usuarios.append(User.objects.get(id=dict['empresa']))
        notificaciones_noleidas = get_cant_notificaciones(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/user_main_notification.html', {
        'form_search': searchbox,
        'notificaciones_recibidas': usuarios,
        'notificaciones_noleidas': notificaciones_noleidas,},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def notification_by_company(request, company_id):
    searchbox = SearchBox()
    try:
        notificaciones_recibidas = request.user.notificaciones_recibidas.filter(
            empresa=company_id)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/notifications_by_company.html', {
        'form_search': searchbox,
        'notificaciones_recibidas': notificaciones_recibidas},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def ver_notificacion(request, notificacion_id):
    searchbox = SearchBox()
    try:
        notificaciones = Notificacion.objects.get(id=notificacion_id)
        notificaciones.estado = "leido"
        notificaciones.save()
        notificaciones_noleidas = get_cant_notificaciones(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('social/ver_notificaciones.html', {
        'form_search': searchbox,
        'notificacion': notificaciones,
        'notificaciones_noleidas': notificaciones_noleidas,},
        context_instance=RequestContext(request))
