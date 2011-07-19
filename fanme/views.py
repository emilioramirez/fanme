from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect


def redirect(request):
    return HttpResponseRedirect("/register/")


def dashboard(request):
    return render_to_response('dashboard.html')
