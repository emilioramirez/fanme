from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


def redirect(request):
    return HttpResponseRedirect("/accounts/user/")


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render_to_response('base.html', context_instance=RequestContext(request))
