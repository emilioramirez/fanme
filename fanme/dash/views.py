from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from fanme.dash.forms import SearchBox
from fanme.items.models import Item
from fanme.accounts.models import Persona, Empresa
from fanme.segmentation.models import Topico
from django.db.models import Q


@login_required(login_url='/accounts/user/')
def dashboard(request):
    searchbox = SearchBox()
    try:
        user = User.objects.get(id=request.user.id)
        profile = user.persona
        items_by_topics = []
        item_topic = {}
        for topic in profile.topicos.all():
            item_topic[topic] = Item.objects.filter(topico__exact=topic)
            items_by_topics.append(Item.objects.filter(topico__exact=topic))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'profile': profile, 'items': items_by_topics, 'example': item_topic},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook(request):
    searchbox = SearchBox()
    return render_to_response('dash/logbook.html', {'form_search': searchbox},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def topicos(request):
    searchbox = SearchBox()
    return render_to_response('dash/topicos.html', {'form_search': searchbox},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def results(request):
    searchbox = SearchBox(request.POST)
    if searchbox.is_valid():
        search = searchbox.cleaned_data['string']
        items_result = Item.objects.filter(nombre__icontains=search)
        users_result = User.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search)
        )
        organizations_result = Empresa.objects.filter(
        razon_social__icontains=search)
        topics_result = Topico.objects.filter(nombre__icontains=search)
    else:
        return render_to_response('dash/results.html',
            {'form_search': searchbox},
            context_instance=RequestContext(request))
    return render_to_response('dash/results.html',
        {'form_search': searchbox,
            'items_result': items_result,
            'users_result': users_result,
            'organizations_result': organizations_result,
            'topics_result': topics_result},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def empresa(request):
    searchbox = SearchBox()
    return render_to_response('dash/empresa.html', {'form_search': searchbox},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook_follow_user(request, user_id):
    searchbox = SearchBox()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404
    return render_to_response('dash/follow.html', {'form_search': searchbox,
    'result': user},
        context_instance=RequestContext(request))
