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
        my_profile = request.user.persona
        items_by_topics = []
        for topic in my_profile.topicos.all():
            items_by_topics.append(Item.objects.filter(topico__exact=topic))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'items': items_by_topics},
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
        #Get the 8 first items that match with the search
        first_items = Item.objects.filter(nombre__icontains=search)[:8]
        #Get the 8 first users that match with the search
        first_users = User.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search),
            ~Q(id=request.user.id))
        #Get the 8 first organizations that match with the search
        first_organizations = Empresa.objects.filter(
        razon_social__icontains=search)[:8]
        #Get the 8 first topics that match with the search
        first_topics = Topico.objects.filter(nombre__icontains=search)[:8]
    else:
        return render_to_response('dash/results.html',
            {'form_search': searchbox},
            context_instance=RequestContext(request))
    return render_to_response('dash/results.html',
        {'form_search': searchbox,
            'items_result': first_items,
            'users_result': first_users,
            'organizations_result': first_organizations,
            'topics_result': first_topics},
            context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def empresa(request):
    searchbox = SearchBox()
    return render_to_response('dash/empresa.html', {'form_search': searchbox},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def follow_user(request, user_id):
    searchbox = SearchBox()
    try:
        user_to_follow = User.objects.get(id=user_id)
        my_profile = request.user.persona
        i_follow = my_profile.following.filter(id=user_id)
        if i_follow:
            return HttpResponseRedirect('/dash/logbook/{0}'.format(user_id))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/follow.html', {'form_search': searchbox,
        'user_to_follow': user_to_follow},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def follow_request(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
        my_profile = request.user.persona
        i_follow = my_profile.following.filter(id=user_id)
        if i_follow:
            return HttpResponseRedirect('/dash/logbook/{0}'.format(user_id))
        else:
            my_profile.following.add(user_to_follow)
            return HttpResponseRedirect('/dash/logbook/{0}'.format(user_id))
    except User.DoesNotExist:
        raise Http404
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa.html/')
    return render_to_response('dash/dashboad.html',
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook_user(request, user_id):
    searchbox = SearchBox()
    try:
        user_logbook = User.objects.get(id=user_id)
        my_profile = request.user.persona
        if not my_profile.following.filter(id=user_logbook.id):
            return HttpResponseRedirect('/dash/follow/{0}'.format(user_id))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/logbook_user.html',
        {'form_search': searchbox, 'user_logbook': user_logbook},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_fans_items(request):
    searchbox = SearchBox()
    messages = []
    try:
        request.user.persona
        messages.append("Sos fan de")
    except Persona.DoesNotExist:
            return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/my_stuff.html',
        {'form_search': searchbox, 'messages': messages,
        'items': request.user.persona.items.all(), 'is_fan': True},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_comments_items(request):
    searchbox = SearchBox()
    messages = []
    try:
        request.user.persona
        messages.append("Has comentado los siguientes items")
    except Persona.DoesNotExist:
            return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/my_stuff.html',
        {'form_search': searchbox, 'messages': messages,
        'items': request.user.item_set.all().distinct(), 'is_fan': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def following(request):
    searchbox = SearchBox()
    messages = ['Estas siguiendo a estos usuarios']
    return render_to_response('dash/following.html',
        {'form_search': searchbox, 'messages': messages},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def followers(request):
    searchbox = SearchBox()
    messages = ['Estos usuarios te estan siguiendo']
    return render_to_response('dash/followers.html',
        {'form_search': searchbox, 'messages': messages},
        context_instance=RequestContext(request))
