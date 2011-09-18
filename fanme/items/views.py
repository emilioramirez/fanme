from django.http import Http404
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from fanme.dash.forms import SearchBox
from fanme.items.models import Item
from fanme.items.forms import ItemRegisterForm
from fanme.accounts.models import Empresa, Persona
from fanme.segmentation.models import Topico


@login_required(login_url='/accounts/user/')
def item(request, item_id):
    searchbox = SearchBox()
    try:
        item = Item.objects.get(pk=item_id)
        user = User.objects.get(pk=request.user.id)
        persona = user.persona
        is_fan = persona.items.filter(nombre=item.nombre)
    except Item.DoesNotExist:
        raise Http404
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'is_fan': is_fan},
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
#        user = User.objects.get(pk=request.user.id)
        persona = request.user.persona
        is_fan = persona.items.filter(nombre=item.nombre)
        if is_fan:
            messages.append("Ya sos fan de {0}".format(item.nombre))
        else:
            persona.items.add(item)
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
        user = User.objects.get(pk=request.user.id)
        persona = user.persona
        persona.items.remove(item)
        messages.append("Ya no sos fan de {0}".format(item.nombre))
    except Item.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa.html/')
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item, 'messages': messages},
        context_instance=RequestContext(request))
