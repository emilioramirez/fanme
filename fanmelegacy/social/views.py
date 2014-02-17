# -*- encoding: utf-8 -*-
from itertools import chain
from operator import attrgetter
from datetime import datetime, date

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse

from social.forms import MessageForm, MessageResponseForm
from social.forms import MessageQueryForm
from social.models import Mensaje
from social.forms import EventoForm, NotificationForm, ConsultaResponseForm
from social.models import Evento, Consulta, Notificacion, EstadoxInvitado

from accounts.models import Persona, Empresa
from accounts.forms import UserLogin

from items.models import Item
from dash.forms import SearchBox
from support.models import TipoNotificacion


@login_required(login_url='/accounts/user/')
def eventos(request):
    searchbox = SearchBox()
    no_hay_eventos = True
    try:
        eventos_creados = request.user.eventos_creados.all().order_by(
            '-fecha_inicio')
    except Evento.DoesNotExist:
        eventos_creados = []
    try:
        eventos_invitado = request.user.eventos_invitado.all().order_by(
            '-fecha_inicio').filter(creador__is_active=True).exclude(estado__exact="finalizado")
        evento_estado_invitado_noleidos = request.user.invitacion_eventos.filter(
            estado="noleido").filter(evento__creador__is_active=True)
        for evento_estado_intivado in evento_estado_invitado_noleidos:
            evento_estado_intivado.estado = "leido"
            evento_estado_intivado.save()
    except Evento.DoesNotExist:
        eventos_invitado = []
    if eventos_creados or eventos_invitado:
        no_hay_eventos = False
    temp = RequestContext(request, {'eventos_creados': eventos_creados,
        'eventos_invitado': eventos_invitado, 'no_hay_eventos': no_hay_eventos,
        'form_search': searchbox,
        'breadcrumb': ["Social", "Eventos"]})
    return render_to_response('social/eventos.html', temp)


@login_required(login_url='/accounts/user/')
def new_evento(request):
    searchbox = SearchBox()
    if request.method == "POST":
        form = EventoForm(request.POST, request.FILES)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        form.fields["invitados"].queryset = users
        latitud = request.POST.get("latitud", "")
        longitud = request.POST.get("longitud", "")
        invitados = request.POST.get("usuarios", "")
        a_split = invitados.split(',')
        usuarios_invitados = []
        for invitado in a_split:
            usuario = User.objects.get(id=invitado)
            usuarios_invitados.append(usuario)
        if form.is_valid():
            evento = form.save(commit=False)
            creador = request.user
            evento.creador = creador
            evento.latitud = latitud
            evento.longitud = longitud
            evento.fecha_creacion = datetime.now()
            try:
                evento.imagen = request.FILES['imagen']
            except KeyError:
                pass
            evento.save()
            messages.add_message(request, messages.SUCCESS, "Evento creado exitosamente")
            form.save_m2m()
            for invitado in usuarios_invitados:
                evento.invitados.add(invitado)
            for invitado in usuarios_invitados:
                evento_x_invitado = EstadoxInvitado()
                evento_x_invitado.evento =  evento
                evento_x_invitado.invitado = invitado
                evento_x_invitado.estado = 'noleido'
                evento_x_invitado.save()
            return HttpResponseRedirect('/social/eventos/')
        else:
            print form.errors
    else:
        form = EventoForm()
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids).filter(is_active=True)
        form.fields["invitados"].queryset = users
    template_vars = RequestContext(request, {"form": form,
        'form_search': searchbox, 'users': users,
        'breadcrumb': ["Social", "Eventos", "Crear"]})
    return render_to_response('social/new_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def evento(request, evento_id):
    searchbox = SearchBox()
    creador = False
    try:
        evento = Evento.objects.get(id=evento_id)
        lista_invitados = evento.invitados.all().filter(is_active=True)
        if (evento.creador == request.user):
            creador = True
    except Evento.DoesNotExist:
        evento = []
    temp = RequestContext(request, {'form_search': searchbox, 'evento': evento,
        'creador': creador, 'lista_invitados': lista_invitados,
        'breadcrumb': ["Social", "Eventos", "Detalle"]})
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
        latitud = request.POST.get("latitud", "")
        longitud = request.POST.get("longitud", "")
        invitados = request.POST.get("usuarios", "")
        a_split = invitados.split(',')
        usuarios_invitados = []
        for invitado in a_split:
            usuario = User.objects.get(id=invitado)
            usuarios_invitados.append(usuario)
        users_invitados = usuarios_invitados
        if form.is_valid():
            evento = form.save(commit=False)
            try:
                evento.imagen = request.FILES['imagen']
            except KeyError:
                pass
            evento.latitud = latitud
            evento.longitud = longitud
            evento.save()
            form.save_m2m()
            for invitado in usuarios_invitados:
                evento.invitados.add(invitado)
                evento_x_invitado = EstadoxInvitado.objects.filter(evento=evento_db).filter(invitado=invitado)
                evento_x_invitado.estado = 'noleido'
                if not evento_x_invitado:
                    evento_x_invitado = EstadoxInvitado()
                    evento_x_invitado.evento =  evento
                    evento_x_invitado.invitado = invitado
                    evento_x_invitado.save()
                else:
                    evento_x_invitado.update()
            return HttpResponseRedirect('/social/eventos/')
    else:
        form = EventoForm(instance=evento_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids).filter(is_active=True)
        form.fields["invitados"].queryset = users
        users_invitados = evento_db.invitados.all()
    template_vars = RequestContext(request, {"form": form, "user": request.user,
        'form_search': searchbox, 'evento': evento_db, 'users': users,
        'users_invitados': users_invitados,
        "breadcrumb": ["Social", "Eventos", "Evento", "Editar"]})
    return render_to_response('social/edit_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def delete_evento(request, evento_id):
    searchbox = SearchBox()
    try:
        evento_db = Evento.objects.get(id=evento_id)
        if (evento_db.creador == request.user):
            if not evento_db.fecha_inicio:
                # Por alguan razon no tiene fecha inicios cuando es obligatorio que lo tenga
                evento_db.fecha_inicio = datetime.now()
            if not evento_db.fecha_fin:
                # Por alguan razon no tiene fecha fin cuando es obligatorio que lo tenga
                evento_db.fecha_fin = datetime.now()
            evento_db.estado = 'cancelado'
            evento_db.save()
        messages.add_message(request, messages.SUCCESS, "El evento ha sido cancelado exitosamente.")
        return HttpResponseRedirect('/social/eventos/')
    except Evento.DoesNotExist:
        return HttpResponseRedirect('/social/eventos/')
    template_vars = RequestContext(request, {
        'form_search': searchbox, 'evento': evento_db})
    return render_to_response('social/edit_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def cancelar_evento(request, evento_id):
    searchbox = SearchBox()
    try:
        evento_db = Evento.objects.get(id=evento_id)
        if (evento_db.creador == request.user):
            evento_db.estado = 'cancelado'
            evento_db.save()
        return HttpResponseRedirect('/social/eventos/')
    except Evento.DoesNotExist:
        return HttpResponseRedirect('/social/eventos/')
    template_vars = RequestContext(request, {
        'form_search': searchbox, 'evento': evento_db})
    return render_to_response('social/edit_evento.html', template_vars)


@login_required(login_url='/accounts/user/')
def mensajes(request):
    searchbox = SearchBox()
    try:
        mensajes_recibidos = request.user.mensajes_recibidos.all().values(
            'user_from').distinct().filter(user_from__is_active=True)
        usuarios = []
        for dict in mensajes_recibidos.all():
            usuarios.append(User.objects.get(id=dict['user_from']))
        msj_noleidos = request.user.mensajes_recibidos.filter(estado="noleido")
        for msj in msj_noleidos:
            msj.estado = "leido"
            msj.save()
        request.user.persona
        template = 'social/messages.html'
    except Persona.DoesNotExist:
        template = 'bussiness/messages_empresa.html'
    return render_to_response(template, {'form_search': searchbox,
        'usuarios': usuarios, 'breadcrumb': ["Social", "Mensajes"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def new_message(request):
    searchbox = SearchBox()
    list_ids = request.user.followers.values_list('user', flat=True)
    users = User.objects.filter(id__in=list_ids).filter(is_active=True)
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
            message.fecha = datetime.now()
            message.save()
            # import pdb; pdb.set_trace()
            messages.add_message(request, messages.SUCCESS, "Tu mensaje ha sido enviado exitosamente")
            form_new_message = MessageForm()
            return HttpResponseRedirect('/social/new_message/')
    else:
        form_new_message = MessageForm()
#        list_ids = request.user.followers.values_list('user', flat=True)
#        users = User.objects.filter(id__in=list_ids)
        form_new_message.fields["user_to_id"].queryset = users
    try:
        request.user.persona
        template = 'social/new_message.html'
    except Persona.DoesNotExist:
        template = 'bussiness/new_message_empresa.html'
    return render_to_response(template,
        {'form_new_message': form_new_message,
        'form_search': searchbox},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def messages_user(request, user_id):
    searchbox = SearchBox()
    if request.method == 'POST':
        form_response_message = MessageResponseForm(request.POST)
        if form_response_message.is_valid():
            mensaje = form_response_message.cleaned_data['mensaje']
            message = Mensaje()
            message.user_from_id = request.user.id
            message.user_to_id = user_id
            message.mensaje = mensaje
            message.fecha = datetime.now()
            message.save()
            form_response_message = MessageResponseForm()
            mensajes = getMensajes(request, user_id)
        else:
            mensajes = getMensajes(request, user_id)
    else:
        mensajes = getMensajes(request, user_id)
        form_response_message = MessageResponseForm()
    return render_to_response('social/messages_user.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes,
        'user_id': user_id,
        'breadcrumb': ["Social", "Mensajes", "Conversacion"]},
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
            messages.add_message(request, messages.SUCCESS, "Tu consulta ha sido enviada exitosamente.")
            form_query_message = MessageQueryForm()
        else:
            items_plan = items_en_plan_vigente(company_id)
            if items_plan == None or items_plan.count() == 0:
                messages.add_message(request, messages.ERROR, "La empresa no posee items registrados. No se le podrá enviar ninguna consulta.")
                no_posee_items = True
            form_query_message.fields["item"].queryset = items_plan
    else:
        form_query_message = MessageQueryForm()
        items_plan = items_en_plan_vigente(company_id)
        if items_plan == None or items_plan.count() == 0:
            messages.add_message(request, messages.ERROR, "La empresa no posee items registrados. No se le podrá enviar ninguna consulta.")
            no_posee_items = True
        else:
            form_query_message.fields["item"].queryset = items_plan
    return render_to_response('social/consulta_a_empresa.html', {
        'form_search': searchbox,
        'company_id': company_id,
        'form_query_message': form_query_message,
        'no_posee_items': no_posee_items},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def responder_consulta(request, item_id, user_id):
    item = Item.objects.get(pk=item_id)
    user = User.objects.get(id__exact=user_id)
    consulta_form = ConsultaResponseForm(request.POST)
    if consulta_form.is_valid():
        respuesta = consulta_form.cleaned_data['respuesta']
        consulta = Consulta()
        consulta.item = item
        consulta.user_from = request.user
        consulta.user_to = user
        consulta.mensaje = respuesta
        consulta.fecha = datetime.now()
        consulta.estado = "noleido"
        consulta.save()
        messages.add_message(request, messages.SUCCESS, "Tu respuesta ha sido enviada exitosamente.")
    try:
        request.user.persona
        url = "../../consulta_empresa/" + user_id + "/" + item_id
    except:
        url = "../../ver_consulta_item_usuario/" + item_id + "/" + user_id
    return HttpResponseRedirect(url)


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
def consultas_usuario(request):
    searchbox = SearchBox()
    consultas_enviadas = request.user.consultas_enviadas.all().values(
        'user_to').distinct().exclude(user_to=request.user)
    usuarios = []
    for dict in consultas_enviadas.all():
        usuarios.append(User.objects.get(id=dict['user_to']))
    return render_to_response('social/consultas.html', {'form_search': searchbox,
        'usuarios': usuarios, 'breadcrumb': ["Social", "Mensajes"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def consultas_usuario_empresas(request, user_id):
    searchbox = SearchBox()
    user = User.objects.filter(pk=user_id)
    consultas_enviadas = request.user.consultas_enviadas.filter(user_to=user).values(
        'item').distinct()
    items = []
    for dict in consultas_enviadas.all():
        items.append(Item.objects.get(id=dict['item']))
    return render_to_response('social/consulta_empresa.html', {'form_search': searchbox,
        'items': items, 'user_id': user_id, 'breadcrumb': ["Social", "Mensajes"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def consultas_empresa_item(request, user_id, item_id):
    searchbox = SearchBox()
    user = User.objects.get(pk=user_id)
    item = Item.objects.get(id=item_id)
    consulta_item1 = Consulta.objects.filter(
        Q(item=item), Q(user_from=user), Q(user_to=request.user))
    consulta_item2 = Consulta.objects.filter(
        Q(item=item), Q(user_from=request.user), Q(user_to=user))
    consulta_item = consulta_item1 | consulta_item2
    consulta_item = consulta_item.order_by('fecha')
    consulta_form = ConsultaResponseForm()
    for consulta in consulta_item.all():
        print user
        if consulta.user_from == user:
            consulta.estado = "leido"
            consulta.save()
    return render_to_response('social/consulta_item.html', {'form_search': searchbox,
        'consulta_form': consulta_form,
        'user_id': user_id, 'item_id': item_id,
        'consulta_item': consulta_item,
        'breadcrumb': ["Social", "Mensajes"]},
        context_instance=RequestContext(request))

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
        'user_from').distinct().exclude(user_from=request.user)
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
        Q(item=item_consultado), Q(user_from=user) | Q(user_to=user))
    for consulta in consulta_item.all():
        if consulta.user_from == user:
            consulta.estado = "leido"
            consulta.save()
    else:
        consulta_form = ConsultaResponseForm()
    consultas_noleidas = request.user.consultas_recibidas.filter(
        estado="noleido").count()
    return render_to_response('social/ver_consulta_item_usuario.html', {
        'form_search': searchbox,
        'usuario': user, 'consultas_noleidas': consultas_noleidas,
        'consulta_item': consulta_item, 'consulta_form': consulta_form,
        'item_id': item_id, 'user_id': user_id},
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
    notificaciones_enviadas = request.user.notificaciones_enviadas.all()
    consultas_noleidas = request.user.consultas_recibidas.filter(
        estado="noleido").count()
    return render_to_response('social/notificaciones.html', {
        'consultas_noleidas': consultas_noleidas,
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
        #form.fields["usuarios_to"].queryset = users
        invitados = request.POST.get("usuarios", "")
        a_split = invitados.split(',')
        usuarios_invitados = []
        for invitado in a_split:
            usuario = User.objects.get(id=invitado)
            usuarios_invitados.append(usuario)
        if form.is_valid():
            notificacion = form.save(commit=False)
            try:
                notificacion.imagen = request.FILES['imagen']
            except KeyError:
                pass
            notificacion.estado = 'actualizado'
            notificacion.save()
            form.save_m2m()
            desinvitados = list(set(notificacion.usuarios_to.all()).difference(usuarios_invitados))
            for invitado in usuarios_invitados:
                notificacion.usuarios_to.add(invitado)
            for desinvitado in desinvitados:
                notificacion.usuarios_to.remove(desinvitado)
                #TODO: aca deberiamos actualizar el estado de cada uno de los usuarios con la notificacion actualizada
            return HttpResponseRedirect('/social/notificaciones/')
    else:
        form = NotificationForm(instance=notificacion_db)
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids)
        users_invitados = notificacion_db.usuarios_to.all()
        #form.fields["invitados"].queryset = users
    template_vars = RequestContext(request, {"form": form, "user": request.user,
        'users_invitados': users_invitados, 'users': users,
        'form_search': searchbox, 'notificacion': notificacion_db})
    return render_to_response('social/edit_notificacion.html', template_vars)


@login_required(login_url='/accounts/user/')
def delete_notificacion(request, notificacion_id):
    searchbox = SearchBox()
    try:
        notificacion_db = Notificacion.objects.get(id=notificacion_id)
        if (notificacion_db.empresa == request.user):
            notificacion_db.estado = 'cancelada'
            notificacion_db.save()
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
        return HttpResponseRedirect(reverse("dash_empresa"))
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
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('social/company_response_message.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def new_notification(request):
    if request.method == "POST":
        form = NotificationForm(request.POST)
        list_ids = request.user.followers.values_list('user', flat=True)        # esto
        users = User.objects.filter(id__in=list_ids)                            # y esto lo podes reemplazar por
        # users = request.user.followers.filter(user__is_active=True)
        invitados = request.POST.get("usuarios", "")                            # y ya que lo usas 2 veces lo podes hacer una vez al comenzar
        a_split = invitados.split(',')                                          # la funcion
        usuarios_invitados = []
        print invitados
        for invitado in a_split:
            usuario = User.objects.get(id=invitado)
            usuarios_invitados.append(usuario)
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
            for invitado in usuarios_invitados:
                notification.usuarios_to.add(invitado)
            return HttpResponseRedirect('/social/notificaciones/')
    else:
        form = NotificationForm()
        list_ids = request.user.followers.values_list('user', flat=True)
        users = User.objects.filter(id__in=list_ids).filter(is_active=True)
    template_vars = RequestContext(request, {"form": form,
        'users': users})
    return render_to_response('social/new_notification.html', template_vars)


@login_required(login_url='/accounts/user/')
def user_main_view_notifications(request):
    notificaciones_recibidas = request.user.notificaciones_recibidas.all()
    dict = {}
    for notificacion in notificaciones_recibidas:
        try:
            dict[notificacion.empresa.empresa].append(notificacion)
        except KeyError:
            dict[notificacion.empresa.empresa] = [notificacion]
    return render_to_response('social/user_main_notification.html', {
        'notificaciones_recibidas': dict,
        'breadcrumb': ["Social", "Notificaciones"]},
                              context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def notification_by_company(request, company_id):
    try:
        notificaciones_recibidas = request.user.notificaciones_recibidas.filter(
            empresa=company_id)
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('social/notifications_by_company.html', {
        'notificaciones_recibidas': notificaciones_recibidas},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def ver_notificacion(request, notificacion_id):
    searchbox = SearchBox()
    try:
        notificaciones = Notificacion.objects.get(id=notificacion_id)
        notificaciones.estado = "leido"
        notificaciones.save()
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('social/ver_notificaciones.html', {
        'form_search': searchbox,
        'notificacion': notificaciones},
        context_instance=RequestContext(request))


def messages_ayuda(request):
    user = request.user
    searchbox = None
    if user.is_authenticated():
        searchbox = SearchBox()
    user_to1 = User()
    user_to1.first_name = 'Fabiana'
    user_to1.last_name = 'Batallanos'
    user_to2 = User()
    user_to2.first_name = 'Paula'
    user_to2.last_name = 'Rivarola'
    usuarios = []
    usuarios.append(user_to1)
    usuarios.append(user_to2)
    form_login = UserLogin()
    return render_to_response('social/messages_ayuda.html', {
        'form_login': form_login,
        'usuarios': usuarios,
        'form_search': searchbox},
        context_instance=RequestContext(request))


def messages_user_ayuda(request):
    user = request.user
    searchbox = None
    if user.is_authenticated():
        searchbox = SearchBox()
    user_to = User()
    user_to.first_name = 'Fabiana'
    user_to.last_name = 'Batallanos'
    user_to.sexo = "F"
    user_from = User()
    user_from.first_name = 'Alan'
    user_from.last_name = 'Karl'
    user_from.sexo = "M"
    mensajes_enviados = []
    mensajes_recibidos = []
    message = Mensaje()
    message.user_from = user_from
    message.user_to = user_to
    message.mensaje = "Hola! como estas?"
    message.fecha = datetime.strptime('Jun 1 2013  1:33PM', '%b %d %Y %I:%M%p')
    mensajes_enviados.append(message)
    message2 = Mensaje()
    message2.user_from = user_to
    message2.user_to = user_from
    message2.mensaje = "Bien, y vos?"
    message2.fecha = datetime.strptime('Jun 2 2013  5:00PM', '%b %d %Y %I:%M%p')
    mensajes_recibidos.append(message2)
    message3 = Mensaje()
    message3.user_from = user_from
    message3.user_to = user_to
    message3.mensaje = "La verdad que no me quejo..."
    message3.fecha = datetime.strptime('Jun 2 2013  5:30PM', '%b %d %Y %I:%M%p')
    mensajes_enviados.append(message3)
    #mensajes_enviados.fecha = datetime.now()
    mensajes = sorted(chain(mensajes_enviados, mensajes_recibidos),
        key=attrgetter('fecha'))
    form_response_message = MessageResponseForm()
    return render_to_response('social/messages_user_ayuda.html', {
        'form_search': searchbox,
        'form_response_message': form_response_message,
        'mensajes': mensajes},
        context_instance=RequestContext(request))


def get_cant_eventos(request):
    return request.user.invitacion_eventos.filter(
            estado='noleido').count()


def eventos_ayuda(request):
    user = request.user
    searchbox = None
    if user.is_authenticated():
        searchbox = SearchBox()
    no_hay_eventos = False
    eventos_creados = []
    primer_evento = Evento()
    primer_evento.descripcion = "Festejo mi cumple!!!"
    primer_evento.estado = "noleido"
    primer_evento.nombre = "Cumple Feliz!"
    primer_evento.direccion = "my-id-tour"
    primer_evento.fecha_creacion = datetime.strptime('Jun 2 2014  5:30PM', '%b %d %Y %I:%M%p')
    primer_evento.fecha_inicio = datetime.strptime('Jun 5 2014  5:30PM', '%b %d %Y %I:%M%p')
    primer_evento.fecha_fin = datetime.strptime('Jun 5 2014  10:30PM', '%b %d %Y %I:%M%p')
    eventos_creados.append(primer_evento)
    segundo_evento = Evento()
    segundo_evento.descripcion = "Chicos nos juntamos para terminar la tesis!"
    segundo_evento.nombre = "Juntada de Tesis"
    segundo_evento.estado = "noleido"
    segundo_evento.fecha_creacion = datetime.strptime('Jun 2 2014  5:30PM', '%b %d %Y %I:%M%p')
    segundo_evento.fecha_inicio = datetime.strptime('Jun 5 2014  5:30PM', '%b %d %Y %I:%M%p')
    segundo_evento.fecha_fin = datetime.strptime('Jun 5 2014  10:30PM', '%b %d %Y %I:%M%p')
    eventos_creados.append(segundo_evento)
    user_invitador = User()
    user_invitador.first_name = 'Carolina'
    user_invitador.last_name = 'Muñoz'
    eventos_invitado = []
    evnto_invitado = Evento()
    evnto_invitado.creador = user_invitador
    evnto_invitado.descripcion = "Nos juntamos a tomar mates!"
    evnto_invitado.estado = "noleido"
    evnto_invitado.nombre = "Mateada"
    evnto_invitado.fecha_inicio = datetime.strptime('Feb 5 2014  5:30PM', '%b %d %Y %I:%M%p')
    evnto_invitado.fecha_fin = datetime.strptime('Feb 5 2014  10:30PM', '%b %d %Y %I:%M%p')
    eventos_invitado.append(evnto_invitado)
    notificaciones_noleidas = 4
    recomendaciones_noleidas = 2
    eventos_noleidos = 1
    temp = RequestContext(request, {'eventos_creados': eventos_creados,
        'eventos_invitado': eventos_invitado, 'no_hay_eventos': no_hay_eventos,
        'form_search': searchbox, 'notificaciones_noleidas': notificaciones_noleidas,
        'recomendaciones_noleidas': recomendaciones_noleidas,
        'eventos_noleidos': eventos_noleidos})
    return render_to_response('social/eventos_ayuda.html', temp)


def evento_ayuda(request):
    user = request.user
    searchbox = None
    if user.is_authenticated():
        searchbox = SearchBox()
    creador = False
    creador = False
    evento = Evento()
    evento.nombre = "Mateada"
    evento.descripcion = "Nos juntamos a tomar mates!"
    evento.fecha_inicio = datetime.strptime('Feb 5 2014  5:30PM', '%b %d %Y %I:%M%p')
    evento.fecha_fin = datetime.strptime('Feb 5 2014  10:30PM', '%b %d %Y %I:%M%p')
    evento.latitud = "-31.40859362873378"
    evento.longitud = "-64.18049812316895"
    evento.direccion = "San Martín 699 Departamento B"
    evento.imagen = "eventos/206_3_2.png"
    lista_invitados = []
    invitado = User()
    invitado.first_name = 'Monica'
    invitado.last_name = 'Quero'
    invitado.email = "moniquero@hotmail.com"
    lista_invitados.append(invitado)
    invitado = User()
    invitado.first_name = 'Vale'
    invitado.last_name = 'Gerez'
    invitado.email = "valegerez@hotmail.com"
    lista_invitados.append(invitado)
    temp = RequestContext(request, {'form_search': searchbox, 'evento': evento,
        'creador': creador, 'lista_invitados': lista_invitados})
    return render_to_response('social/evento_ayuda.html', temp)


def user_main_view_notifications_ayuda(request):
    user = User()
    user.first_name = "Kodak"
    user.last_name = "Kodak"
    empresa = Empresa()
    empresa.user = user
    empresa.razon_social = "Kodak"
    notificaciones_recibidas = []
    notificacion = Notificacion()
    notificacion.empresa = user
    notificaciones_recibidas.append(notificacion)
    dict = {}
    for notificacion in notificaciones_recibidas:
        try:
            dict[notificacion.empresa].append(notificacion)
        except KeyError:
            dict[notificacion.empresa.empresa] = [notificacion]
            print 'a'
    return render_to_response('social/user_main_notification_ayuda.html', {
        'notificaciones_recibidas': dict,
        'breadcrumb': ["Social", "Notificaciones"]},
                              context_instance=RequestContext(request))


def notification_by_company_ayuda(request):
    user = User()
    user.first_name = "Kodak"
    user.last_name = "Kodak"
    empresa = Empresa()
    empresa.user = user
    empresa.razon_social = "Kodak"
    notificaciones_recibidas = []
    notificacion = Notificacion()
    notificacion.empresa = user
    notificacion.nombre = "Promo 2x1"
    notificacion.descripcion = "Llevate dos revelados de fotos al precio de uno"
    notificacion.fecha_expiracion = datetime.strptime('Mar 8 2014  5:30PM', '%b %d %Y %I:%M%p')
    notificaciones_recibidas.append(notificacion)
    notificacion = Notificacion()
    notificacion.empresa = user
    notificacion.nombre = "Promoción albumes"
    notificacion.descripcion = "Con el revelado de mas de 100 fotos te regalamos un album. "
    notificacion.fecha_expiracion = datetime.strptime('Mar 8 2014  5:30PM', '%b %d %Y %I:%M%p')
    notificaciones_recibidas.append(notificacion)
    return render_to_response('social/notifications_by_company_ayuda.html', {
        'notificaciones_recibidas': notificaciones_recibidas},
        context_instance=RequestContext(request))


def ver_notificacion_ayuda(request):
    user = User()
    user.first_name = "Kodak"
    user.last_name = "Kodak"
    empresa = Empresa()
    empresa.user = user
    empresa.razon_social = "Kodak"
    notificacion = Notificacion()
    notificacion.empresa = user
    notificacion.nombre = "Promo 2x1"
    notificacion.descripcion = "Llevate dos revelados de fotos al precio de uno"
    notificacion.fecha_desde = datetime.strptime('Feb 8 2014  5:30PM', '%b %d %Y %I:%M%p')
    notificacion.fecha_expiracion = datetime.strptime('Mar 8 2014  5:30PM', '%b %d %Y %I:%M%p')
    return render_to_response('social/ver_notificacion_ayuda.html', {
        'notificacion': notificacion},
        context_instance=RequestContext(request))