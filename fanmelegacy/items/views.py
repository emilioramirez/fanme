# -*- coding: utf-8 *-*
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from datetime import datetime, date
from items.forms import ItemRegisterForm, CommentForm
from accounts.models import Empresa, Persona
from items.models import Item, Comentario, Recomendacion, ItemDenuncias
from items.models import ItemImagen
from rathings.models import Dislike
from segmentation.models import Topico
from social.models import Actividad
from bussiness.models import PlanXEmpresa
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import comments
from django.contrib.comments.views.moderation import perform_delete
from django.contrib.comments.views.utils import next_redirect
from django.contrib.contenttypes.models import ContentType


@login_required(login_url='/accounts/user/')
def item(request, item_id):
    # comment_form = CommentForm()
    mostrar_boton_enlace = True
    is_fan = False
    item = None

    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404

    item_plan = PlanXEmpresa.objects.filter(item=item)
    empresas = []
    for enlace_externo in item_plan:
        if enlace_externo.fecha_fin_vigencia > date.today():
            empresa = Empresa.objects.get(user_id=enlace_externo.empresa.id)
            empresas.append(empresa)
    mostrar_denuncia = verificar_si_existe_denuncia(request, item)

    try:
        request.user.empresa
        mostrar_boton_enlace = puede_registrar_enlace(request, item)
    except Empresa.DoesNotExist:
        is_fan = request.user.persona.items.filter(pk=item.pk).exists()
        mostrar_boton_enlace = False
    
    return render_to_response('items/item.html',
        {'item': item, 'is_fan': is_fan,
        # 'comment_form': comment_form,
        'empresas': empresas,
        'mostrar_boton_enlace': mostrar_boton_enlace,
        'mostrar_denuncia': mostrar_denuncia},
        context_instance=RequestContext(request))


def puede_registrar_enlace(request, item):
    ret = False
    planes = request.user.plan_empresa.all().order_by('-fecha_fin_vigencia')
    if not planes:
        messages.add_message(request, messages.INFO, 'No posee ningún plan.')
    else:
        plan = planes[0]
        cant_items = plan.plan.cant_items
        count = plan.item.count()
        if plan.fecha_fin_vigencia < date.today():
            messages.add_message(request, messages.INFO, 'El plan seleccionado ha expirado. Seleccione un nuevo plan.')
        else:
            try:
                plan.item.get(pk=item.id)
                messages.add_message(request, messages.INFO, 'Este ítem ya tiene registrado el enlace externo de la empresa.')
            except:
                if count >= cant_items:
                    messages.add_message(request, messages.INFO, 'La cantidad de items del plan seleccionado ha llegado a su límite. No podrá registrar el enclace externo en el ítem.')
                    ret = False
                else:
                    ret = True
    return ret


@login_required(login_url='/accounts/user/')
def empresa(request, empresa_id):
    try:
        user_empresa = User.objects.get(pk=empresa_id)
        planes = user_empresa.plan_empresa.filter(fecha_fin_vigencia__gt=date.today()).order_by('-fecha_fin_vigencia')
        items_plan = None
        if planes:
            plan = planes[0]
            if plan.fecha_fin_vigencia > date.today():
                items_plan = plan.item.all()
    except User.DoesNotExist:
        messages.add_message(request, messages.WARNING, "El usuario que intentas acceder no existe")
        return HttpResponseRedirect(reverse("dashboard"))
    try:
        i_follow = request.user.persona.following.get(id=empresa_id)
    except User.DoesNotExist:
        i_follow = False
    return render_to_response('dash/empresa.html',
        {'user_empresa': user_empresa, 'planes': planes,
         'items_plan': items_plan, 'i_follow': i_follow}
        , context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def register_item(request):
    if request.method == 'POST':
        form_register = ItemRegisterForm(request.POST, request.FILES)
        if form_register.is_valid():
            nombre = form_register.cleaned_data['nombre']
            descripcion = form_register.cleaned_data['descripcion']
            topico = form_register.cleaned_data['topico']
            item = Item()
            item.nombre = nombre
            item.descripcion = descripcion
            item.topico = Topico.objects.get(nombre=topico)
            item.cantidad_fans = 0
            try:
                profile.avatar = request.FILES['avatar']
            except KeyError:
                print 'Excepcion en social/view.edit_account'
            item.save()
            try:
                imagen = request.FILES['imagen']
                itemimagen = ItemImagen()
                itemimagen.item = item
                itemimagen.imagen = imagen
                itemimagen.save()
            except KeyError:
                print 'Excepcion en items/view.register_item'
            messages.add_message(request, messages.SUCCESS, "Se creo el Item exitosamente")
            form_register = ItemRegisterForm()
    else:
        form_register = ItemRegisterForm()
    return render_to_response('items/register_item.html',
        {'form_register': form_register, "breadcrumb": ["Item", "Registrar nuevo"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def fan(request, item_id):
    comment_form = CommentForm()
    try:
        item = Item.objects.get(pk=item_id)
        is_fan = request.user.persona.items.filter(nombre=item.nombre)
        if is_fan:
            messages.add_message(request, messages.INFO, u"Ya sos fan de {0}".format(item.nombre))
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
            messages.add_message(request, messages.SUCCESS, u"Te has hecho fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('items/item.html',
        {'item': item, 'is_fan': is_fan,
        'comment_form': comment_form, },
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def unfan(request, item_id):
    comment_form = CommentForm()
    try:
        item = Item.objects.get(pk=item_id)
        request.user.persona.items.remove(item)
        if (item.cantidad_fans > 0):
            item.cantidad_fans -= 1
        item.save()
        request.user.save()
        messages.add_message(request, messages.SUCCESS, u"Ya no sos fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('items/item.html',
        {'item': item, 'comment_form': comment_form},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendation(request, item_id):
    usuarios_ya_recomendados = request.user.recomendaciones_enviadas.filter(
        item=item_id).values_list('user_destino', flat=True)
    seguidores = request.user.followers.exclude(user__in=usuarios_ya_recomendados)
    #seguidores_activos = seguidores.filter(is_active=True)
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
                actividad.usuario_destino = usuario
                actividad.recomendacion = recomendacion
                actividad.save()
        messages.add_message(request, messages.SUCCESS, u"Se han enviado las recomendaciones correctamente.")
    if not seguidores and not usuarios_ya_recomendados:
        messages.add_message(request, messages.ERROR, u"Para realizar una recomendacion al menos un usuario debe seguirlo.")
    return render_to_response('items/recomendacion.html',
        {'usuarios': seguidores, 'item': item, "breadcrumb": ["Item", "Recomendar"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user')
def delete_own_comment(request, comment_id, next=None):
    comment = get_object_or_404(comments.get_model(), id=comment_id)
    if comment.user.id != request.user.id:
        raise Http404
    perform_delete(request, comment)
    messages.add_message(request, messages.SUCCESS, u"Sé ha eliminado tu comentario con éxito.")
    return HttpResponseRedirect(reverse("item-detail", args=[comment.object_pk]))


@login_required(login_url='/accounts/user')
def denunciar_item(request, item_id):
    comment_form = CommentForm()
    item = Item.objects.get(pk=item_id)
    denuncia = ItemDenuncias()
    denuncia.item = Item.objects.get(pk=item_id)
    denuncia.user = request.user
    denuncia.save()
    mostrar_denuncia = verificar_si_existe_denuncia(request, item)
    return render_to_response('items/item.html',
        {'item': item, 'comment_form': comment_form, 'comments': comments,
        'mostrar_denuncia': mostrar_denuncia},
        context_instance=RequestContext(request))


def verificar_si_existe_denuncia(request, item):
    disklike = Dislike.objects.filter(
        object_id=item.pk,
        content_type=ContentType.objects.get_for_model(Item))
    if disklike:
        return False
    return True