# -*- coding: utf-8 *-*
from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import datetime, date

from dash.forms import SearchBox
from items.models import Item, Comentario, Marca, Recomendacion
from items.models import ItemImagen
from items.forms import ItemRegisterForm, CommentForm
from accounts.models import Empresa, Persona
from segmentation.models import Topico
from social.models import Actividad
from bussiness.models import PlanXEmpresa


@login_required(login_url='/accounts/user/')
def item(request, item_id):
    searchbox = SearchBox()
    comment_form = CommentForm()
    try:
        item = Item.objects.get(pk=item_id)
        #is_fan = request.user.persona.items.filter(nombre=item.nombre)
        is_fan = False
        item_plan = PlanXEmpresa.objects.filter(item=item)
        mostrar_boton_enlace = True
        try:
            request.user.persona
        except:
            mostrar_boton_enlace = puede_registrar_enlace(request, item)
        empresas = []
        for enlace_externo in item_plan:
            if enlace_externo.fecha_fin_vigencia > date.today():
                empresa = Empresa.objects.get(user_id=enlace_externo.empresa.id)
                empresas.append(empresa)
        if item.enlaces_externos.count:
            print item.enlaces_externos
        comments = item.comentarios_recibidos.all().order_by('fecha')
    except Item.DoesNotExist:
        raise Http404
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'is_fan': is_fan, 'comment_form': comment_form,
        'comments': comments, 'empresas': empresas,
        'mostrar_boton_enlace': mostrar_boton_enlace},
        context_instance=RequestContext(request))


def puede_registrar_enlace(request, item):
    ret = False
    planes = request.user.plan_empresa.all().order_by('-fecha_fin_vigencia')
    if not planes:
        ret = True
    else:
        plan = planes[0]
        if plan.fecha_fin_vigencia < date.today():
            ret = True
    return ret


@login_required(login_url='/accounts/user/')
def empresa(request, empresa_id):
    searchbox = SearchBox()
    try:
        empresa = Empresa.objects.get(pk=empresa_id)
    except Empresa.DoesNotExist:
        raise Http404
    return render_to_response('items/empresa.html', {'form_search': searchbox,
        'empresa': empresa}, context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def register_item(request):
    searchbox = SearchBox()
    messages = []
    if request.method == 'POST':
        form_register = ItemRegisterForm(request.POST, request.FILES)
        if form_register.is_valid():
            nombre = form_register.cleaned_data['nombre']
            descripcion = form_register.cleaned_data['descripcion']
            topico = form_register.cleaned_data['topico']
#            marca = form_register.cleaned_data['marca']
            item = Item()
            item.nombre = nombre
            item.descripcion = descripcion
            item.topico = Topico.objects.get(nombre=topico)
            item.cantidad_fans = 0
            try:
                profile.avatar = request.FILES['avatar']
            except KeyError:
                print 'Excepcion en social/view.edit_account'
#            item.marca = Marca.objects.get(nombre=marca)
            item.save()
            try:
                imagen = request.FILES['imagen']
                itemimagen = ItemImagen()
                itemimagen.item = item
                itemimagen.imagen = imagen
                itemimagen.save()
            except KeyError:
                print 'Excepcion en items/view.register_item'
            messages.append("Se creo el Item exitosamente")
            form_register = ItemRegisterForm()
    else:
        form_register = ItemRegisterForm()
    return render_to_response('items/register_item.html',
        {'form_search': searchbox,
        'form_register': form_register,
        'messages': messages},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def fan(request, item_id):
    searchbox = SearchBox()
    comment_form = CommentForm()
    messages = []
    try:
        item = Item.objects.get(pk=item_id)
        is_fan = request.user.persona.items.filter(nombre=item.nombre)
        comments = item.comentarios_recibidos.all().order_by('fecha')
        if is_fan:
            messages.append(u"Ya sos fan de {0}".format(item.nombre))
        else:
            request.user.persona.items.add(item)
            item.cantidad_fans += 1
            item.save()
            request.user.save()
            is_fan = True
            #Registro la actividad del usuario
            actividad = Actividad()
            actividad.descripcion = "se hizo fan de "
            actividad.tipo = "fan"
            actividad.fecha = datetime.now()
            actividad.item = item
            actividad.usuario_origen = request.user
            actividad.save()
            messages.append(u"Te has hecho fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'messages': messages, 'is_fan': is_fan,
        'comment_form': comment_form, 'comments': comments},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def unfan(request, item_id):
    searchbox = SearchBox()
    comment_form = CommentForm()
    messages = []
    try:
        item = Item.objects.get(pk=item_id)
        request.user.persona.items.remove(item)
        if (item.cantidad_fans > 0):
            item.cantidad_fans -= 1
        item.save()
        request.user.save()
        messages.append(u"Ya no sos fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'messages': messages, 'comment_form': comment_form},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def comment(request, item_id):
    searchbox = SearchBox()
    messages = []
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comentario_text = comment_form.cleaned_data['texto']
            comentario = Comentario()
            comentario.comentario = comentario_text
            comentario.item = item
            comentario.user = request.user
            comentario.fecha = datetime.now()
            comentario.me_gusta = 0
            comentario.denuncias = 0
            comentario.save()
            messages.append(u"Has comentado el producto {0}".format(
                item.nombre))
            comment_form = CommentForm()
            actividad = Actividad()
            actividad.descripcion = "realizo un comentario en "
            actividad.tipo = "comentario"
            actividad.fecha = datetime.now()
            actividad.item = item
            actividad.usuario_origen = request.user
            actividad.comentario = comentario
            actividad.save()
    else:
        comment_form = CommentForm()
    comments = item.comentarios_recibidos.all().order_by('fecha')
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'comment_form': comment_form, 'messages': messages,
        'comments': comments},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendation(request, item_id):
    searchbox = SearchBox()
    usuarios_ya_recomendados = request.user.recomendaciones_enviadas.filter(
        item=item_id).values_list('user_destino', flat=True)
    seguidores = request.user.followers.exclude(user__in=usuarios_ya_recomendados)
    usuarios = []
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404
    if request.method == 'POST':
        lista_ids = request.POST.getlist('recomendados')
        for id in lista_ids:
            usuarios.append(User.objects.get(id=id))
        for usuario in usuarios:
            try:
                recomendaciones = request.user.recomendaciones_enviadas.filter(
                    user_destino=usuario.id, item=item)
                if recomendaciones.count() == 0:
                    raise Recomendacion.DoesNotExist
            except Recomendacion.DoesNotExist:
                recomendacion = Recomendacion()
                recomendacion.item = item
                recomendacion.user_destino = usuario
                recomendacion.fecha = datetime.now()
                recomendacion.user_origen = request.user
                recomendacion.save()
                item.save()
                actividad = Actividad()
                actividad.descripcion = "recomendo el siguiente item"
                actividad.tipo = "recomendacion"
                actividad.fecha = datetime.now()
                actividad.item = item
                actividad.usuario_origen = request.user
                actividad.recomendacion = recomendacion
                actividad.save()
        return HttpResponseRedirect('/dash/dashboard/')
    return render_to_response('items/recomendacion.html',
        {'form_search': searchbox, 'usuarios': seguidores, 'item': item},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def me_gusta_comentario(request, comentario_id):
    try:
        comentario = Comentario.objects.get(pk=comentario_id)
    except Comentario.DoesNotExist:
        raise Http404
    comentario.me_gusta += 1
    comentario.save()
#    comments = item.comentario_set.all().order_by('fecha')
    return HttpResponseRedirect('/items/item/{0}'.format(comentario.item.id))
#    return render_to_response('items/item.html', {'form_search': searchbox,
#        'item': item, 'comment_form': comment_form, 'messages': messages,
#        'comments': comments},
#        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def denunciar_comentario(request, comentario_id):
    try:
        comentario = Comentario.objects.get(pk=comentario_id)
    except Comentario.DoesNotExist:
        raise Http404
    comentario.denuncias += 1
    comentario.save()
    return HttpResponseRedirect('/items/item/{0}'.format(comentario.item.id))
