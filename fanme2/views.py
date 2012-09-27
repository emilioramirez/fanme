from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


def home(request):
    return render_to_response('login.html', 
        context_instance=RequestContext(request))
