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
        item_topic = {}
        for topic in my_profile.topicos.all():
            item_topic[topic] = Item.objects.filter(topico__exact=topic)
            items_by_topics.append(Item.objects.filter(topico__exact=topic))
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'items': items_by_topics, 'example': item_topic},
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
        user = User.objects.get(id=request.user.id)
        #Get the 8 first items that match with the search
        items_result = Item.objects.filter(nombre__icontains=search)
        first_items = count_items(items_result)
        #Get the 8 first users that match with the search
        users_result_intermediate = User.objects.filter(
            Q(first_name__icontains=search) | Q(last_name__icontains=search))
        users_result = verify_user(user, users_result_intermediate)
        first_users = count_items(users_result)
        #Get the 8 first organizations that match with the search
        organizations_result = Empresa.objects.filter(
        razon_social__icontains=search)
        first_organizations = count_items(organizations_result)
        #Get the 8 first topics that match with the search
        topics_result = Topico.objects.filter(nombre__icontains=search)
        first_topics = count_items(topics_result)
    else:
        return render_to_response('dash/results.html',
            {'form_search': searchbox},
            context_instance=RequestContext(request))
    return render_to_response('dash/results.html',
        {'form_search': searchbox,
            'items_result': first_items,
            'users_result': first_users,
            'organizations_result': first_organizations,
            'topics_result': first_topics,
            'user': user},
        context_instance=RequestContext(request))


def count_items(items_result):
    list_items = []
    i = 1
    for items in items_result:
        if i <= 8:
            list_items.append(items)
            i = i + 1
        else:
            break
    return list_items
    #print len(list_items)


def verify_user(user, user_result_intermediate):
    users_result = []
    for users in user_result_intermediate:
        if user.id != users.id:
            users_result.append(users)
    return users_result


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
    return render_to_response('dash/my_fans_items.html',
        {'form_search': searchbox, 'messages': messages},
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
    print request.user.followers.all()
    messages = ['Estos usuarios te estan siguiendo']
    return render_to_response('dash/followers.html',
        {'form_search': searchbox, 'messages': messages},
        context_instance=RequestContext(request))
