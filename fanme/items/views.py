from django.http import Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from fanme.dash.forms import SearchBox
from fanme.items.models import Item
from fanme.accounts.models import Empresa


@login_required(login_url='/accounts/user/')
def item(request, item_id):
    searchbox = SearchBox()
    try:
        item = Item.objects.get(pk=item_id)
    except Item.DoesNotExist:
        raise Http404
    return render_to_response('items/item.html', {'form_search': searchbox,
        'item': item}, context_instance=RequestContext(request))
        
 
@login_required(login_url='/accounts/user/')
def empresa(request, empresa_id):
    searchbox = SearchBox()
    try:
        empresa = Empresa.objects.get(pk=empresa_id)
    except Empresa.DoesNotExist:
        raise Http404
    return render_to_response('items/empresa.html', {'form_search': searchbox,
        'empresa': empresa}, context_instance=RequestContext(request))
