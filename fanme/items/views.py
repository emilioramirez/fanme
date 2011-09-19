from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from datetime import datetime

from fanme.dash.forms import SearchBox
from fanme.items.models import Item, Comentario
from fanme.items.forms import ItemRegisterForm, CommentForm
from fanme.accounts.models import Empresa, Persona
from fanme.segmentation.models import Topico


@login_required(login_url='/accounts/user/')
def item(request, item_id):
    searchbox = SearchBox()
    comment_form = CommentForm()
    try:
        item = Item.objects.get(pk=item_id)
        is_fan = request.user.persona.items.filter(nombre=item.nombre)
        comments = item.comentario_set.all().order_by('fecha')
        print comments
    except Item.DoesNotExist:
        raise Http404
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'is_fan': is_fan, 'comment_form': comment_form,
        'comments': comments},
        context_instance=RequestContext(request))


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
    if request.method == 'POST':
        form_register = ItemRegisterForm(request.POST)
        if form_register.is_valid():
            nombre = form_register.cleaned_data['nombre']
            descripcion = form_register.cleaned_data['descripcion']
            topico = form_register.cleaned_data['topico']
            item = Item()
            item.nombre = nombre
            item.descripcion = descripcion
            item.topico = Topico.objects.get(nombre=topico)
            item.save()
    else:
        form_register = ItemRegisterForm()
    return render_to_response('items/register_item.html',
        {'form_search': searchbox,
        'form_register': form_register},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def fan(request, item_id):
    searchbox = SearchBox()
    messages = []
    try:
        item = Item.objects.get(pk=item_id)
        is_fan = request.user.persona.items.filter(nombre=item.nombre)
        if is_fan:
            messages.append("Ya sos fan de {0}".format(item.nombre))
        else:
            request.user.persona.items.add(item)
            is_fan = True
            messages.append("Te has hecho fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa.html/')
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'messages': messages, 'is_fan': is_fan},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def unfan(request, item_id):
    searchbox = SearchBox()
    messages = []
    try:
        item = Item.objects.get(pk=item_id)
        request.user.persona.items.remove(item)
        messages.append("Ya no sos fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa.html/')
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'messages': messages},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def comment(request, item_id):
    searchbox = SearchBox()
    messages = []
    if request.method == 'POST':
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            try:
                item = Item.objects.get(pk=item_id)
                comentario_text = form_comment.cleaned_data['texto']
                comentario = Comentario()
                comentario.comentario = comentario_text
                comentario.item = item
                comentario.user = request.user
                comentario.fecha = datetime.now()
                comentario.save()
                messages.append("Has comentado el producto {0}".format(
                    item.nombre))
                comment_form = CommentForm()
                comments = item.comentario_set.all().order_by('fecha')
            except Item.DoesNotExist:
                raise Http404
            except Persona.DoesNotExist:
                return HttpResponseRedirect('/dash/empresa.html/')
    else:
        comment_form = CommentForm()
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'comment_form': comment_form, 'messages': messages,
        'comments': comments},
        context_instance=RequestContext(request))
