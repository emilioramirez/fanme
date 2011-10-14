from django.shortcuts import render_to_response
from fanme.dash.forms import SearchBox
from django.template import RequestContext
from fanme.social.forms import EventoForm


def eventos(request):
    pass


def new_evento(request):
    searchbox = SearchBox()
    form = EventoForm()
    return render_to_response('social/new_evento.html',
        {'form_search': searchbox, 'form': form},
        context_instance=RequestContext(request))
