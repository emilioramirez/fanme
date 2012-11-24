from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response


def profile(request):
    context = {'profile': 'profile'}
    return render_to_response('profile.html', context,
        context_instance=RequestContext(request))