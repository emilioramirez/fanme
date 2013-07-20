from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def item(request):
    return render_to_response('core/item.html',
            context_instance=RequestContext(request))


@login_required
def create_item(request):
    return render_to_response('item.html',
            context_instance=RequestContext(request))
