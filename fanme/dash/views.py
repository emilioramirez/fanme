from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from fanme.dash.forms import SearchBox
from fanme.accounts.models import Persona


@login_required(login_url='/accounts/user/')
def dashboard(request):
    searchbox = SearchBox()
    #~ if request.user.is_authenticated():
        #~ profile = Persona.objects.get(user=request.user)
        #~ birt = profile.fecha_nacimiento
    #~ else:
        #~ # Do something for anonymous users.
        #~ pass
    return render_to_response('dash/dashboard.html',
                            {'form_search': searchbox},
                            context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook(request):
    searchbox = SearchBox()
    return render_to_response('dash/logbook.html',
                            {'form_search': searchbox},
                            context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def topicos(request):
    searchbox = SearchBox()
    return render_to_response('dash/topicos.html',
                            {'form_search': searchbox},
                            context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def results(request):
    searchbox = SearchBox()
    return render_to_response('dash/results.html',
                            {'form_search': searchbox},
                            context_instance=RequestContext(request))
