# -*- encoding: utf-8 -*-
import operator
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django import forms

from dash.forms import SearchBox, UserUpdateForm, PassUpdateForm
from items.models import Item
from accounts.models import Persona, Empresa
from segmentation.models import Topico
from items.models import Recomendacion
from fanmelegacy import recommendations
from accounts.forms import UserLogin
from itertools import chain
from operator import attrgetter
from django.contrib.auth import logout


@login_required(login_url='/accounts/user/')
def dashboard(request):
    searchbox = SearchBox()
    try:
        my_profile = request.user.persona
        #block recommendation
        recommendations.diccionario = recommendations.getMatrix()
        ranking = recommendations.getRecommendations(
            recommendations.diccionario, request.user.username)
        #block recommendation
        root_topics = Topico.objects.filter(padre=None)
        items_by_topics = []
        if ranking == []:
            for topic in my_profile.topicos.all():
                lista = Item.objects.filter(topico__exact=topic).order_by(
                    '-cantidad_fans')
                items_by_topics.append(lista)
        else:
            for rank, itemname in ranking:
                lista = Item.objects.filter(nombre=itemname)
                items_by_topics.append(lista)
        notificaciones_noleidas = get_cant_notificaciones(request)
        recomendaciones_noleidas = get_cant_recomendaciones(request)
        mensajes_nolidas = get_cant_mensajes(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'topicos': items_by_topics,
        'notificaciones_noleidas': notificaciones_noleidas,
        'recomendaciones_noleidas': recomendaciones_noleidas,
        'mensajes_nolidas':mensajes_nolidas,
        'r_topics': root_topics},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def dashboard_topic(request, topic_id):
    searchbox = SearchBox()
    lista = []
    try:
        #block recommendation
        recommendations.diccionario = recommendations.getMatrix()
        ranking = recommendations.getRecommendations(
            recommendations.diccionario, request.user.username)
        #block recommendation
        root_topics = Topico.objects.filter(padre=None)
        topico = Topico.objects.get(id=topic_id)
        yes = request.user.persona.topicos.get(id=topic_id)
#        if yes:
#            lista.append(Item.objects.filter(topico__exact=topico).order_by(
#                '-cantidad_fans'))
        if yes:
            if ranking != []:
                for rank, itemname in ranking:
                    lista.append(Item.objects.filter(nombre=itemname,
                        topico__exact=topico).order_by('-cantidad_fans'))
            else:
                lista.append(Item.objects.filter(topico__exact=topico).order_by(
                '-cantidad_fans'))

    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    except Topico.DoesNotExist:
        return render_to_response('dash/dashboard.html',
            {'form_search': searchbox, 'topicos': lista,
                'r_topics': root_topics},
            context_instance=RequestContext(request))
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'topicos': lista, 'r_topics': root_topics},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def dashboard_topic_add(request, topic_id):
    try:
        top = Topico.objects.get(id=topic_id)
        profile = request.user.persona
        profile.topicos.add(top)
        profile.save()
    except Topico.DoesNotExist:
        pass
    except Persona.DoesNotExist:
        pass
    return HttpResponseRedirect('/dash/dashboard/')


@login_required(login_url='/accounts/user/')
def logbook(request):
    searchbox = SearchBox()
    try:
        followings = request.user.persona.following.all()
        actividades = []
        for user in followings:
            actividades = sorted(
                chain(
                    user.act_origen.all(), actividades),
                key=attrgetter('fecha'), reverse=True)
        notificaciones_noleidas = get_cant_notificaciones(request)
        recomendaciones_noleidas = get_cant_recomendaciones(request)
        mensajes_nolidas = get_cant_mensajes(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/logbook.html', {'form_search': searchbox,
        'notificaciones_noleidas': notificaciones_noleidas,
        'recomendaciones_noleidas': recomendaciones_noleidas,
        'mensajes_nolidas':mensajes_nolidas,
        'actividades': actividades}, context_instance=RequestContext(request))


def get_cant_notificaciones(request):
    return request.user.notificaciones_recibidas.filter(~Q(estado='leido')).count()
            #estado='noleido').count()


def get_cant_recomendaciones(request):
    return request.user.recomendaciones_recibidas.filter(
            estado='noleido').count()


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
        list_of_words = search.strip().split(" ")
        # Get the 8 first items that match with the search
        # reduce(operator.or_, (Q(first_name__contains=x) for x in ['x', 'y', 'z']))
        # Model.objects.filter(reduce(...))
        # Is equivalent to:
        # Model.objects.filter(Q(first_name__contains='x') | Q(first_name__contains='y') | Q(first_name__contains='z'))
        first_items = Item.objects.filter(
                        reduce(operator.or_,
                              (Q(nombre__icontains=x) for x in list_of_words)
                        )
                    )[:8]
        first_users = User.objects.filter(
                    reduce(operator.or_,
                          (Q(first_name__icontains=x) | Q(last_name__icontains=x) for x in list_of_words)
                    ),
                    ~Q(id=request.user.id))
        active_users = first_users.filter(is_active=True)
        #Get the 8 first organizations that match with the search
        first_organizations = Empresa.objects.filter(
                reduce(operator.or_,
                      (Q(razon_social__icontains=x) for x in list_of_words)
                )
            )[:8]
        #Get the 8 first topics that match with the search
        first_topics = Topico.objects.filter(
                reduce(operator.or_,
                      (Q(nombre__icontains=x) for x in list_of_words)
                )
            )[:8]
    else:
        return render_to_response('dash/results.html',
            {'form_search': searchbox},
            context_instance=RequestContext(request))
    return render_to_response('dash/results.html',
        {'form_search': searchbox,
            'items_result': first_items,
            'users_result': active_users,
            'organizations_result': first_organizations,
            'topics_result': first_topics},
            context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def empresa(request):
    searchbox = SearchBox()
    messages = ['Estos usuarios se han hecho fan']
    return render_to_response('bussiness/dash_empresa.html', {'form_search': searchbox,
        'messages': messages},
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
        'user_logbook': user_to_follow},
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
        print user_logbook
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
    lista = []
    try:
        items = request.user.persona.items.all()
        for item in items:
            lista.append(
                (item, 0)
            )
        messages.append("Sos fan de")
    except Persona.DoesNotExist:
            return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mi_fanes.html',
        {'form_search': searchbox, 'messages': messages,
        'items': lista, 'is_fan': True},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_comments_items(request):
    searchbox = SearchBox()
    messages = []
    lista = []
    try:
        request.user.persona
        items = request.user.items_comentados.all().distinct()
        for item in items:
            lista.append(
                (item,
                request.user.comentarios_realizados.filter(item=item).count()
                )
            )
        messages.append("Has comentado los siguientes items")
    except Persona.DoesNotExist:
            return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mis_comentarios.html',
        {'form_search': searchbox, 'messages': messages,
        'items': lista, 'is_fan': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendaciones_enviadas(request):
    searchbox = SearchBox()
    messages = []
    try:
        request.user.persona
        items_ids = request.user.recomendaciones_enviadas.all().values_list(
            'item', flat=True).distinct()
        items = Item.objects.filter(id__in=items_ids)
        messages.append("Has recomendado los siguientes items")
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    recomendaciones = request.user.recomendaciones_enviadas.all().order_by(
        'fecha')
    return render_to_response('dash/mis_recomendaciones_enviadas.html',
        {'form_search': searchbox, 'messages': messages,
        'recomendaciones': items,
            'is_fan': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendaciones_recibidas(request):
    searchbox = SearchBox()
    messages = []
    try:
        request.user.persona
        items_ids = request.user.recomendaciones_recibidas.all().values_list(
            'item', flat=True).distinct()
        items = Item.objects.filter(id__in=items_ids)
        rec = request.user.recomendaciones_recibidas.filter(estado="noleido")
        for r in rec:
            r.estado = "leido"
            r.save()
        messages.append("Te han recomendado los siguientes items")
        notificaciones_noleidas = get_cant_notificaciones(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mis_recomendaciones_recibidas.html',
        {'form_search': searchbox, 'messages': messages,
        'recomendaciones': items,
        'notificaciones_noleidas': notificaciones_noleidas, 'is_fan': False},
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


@login_required(login_url='/accounts/user/')
def edit_account(request):
    searchbox = SearchBox()
    messages = []
    is_active = True
    try:
        data = {'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'sex': request.user.persona.sexo,
                    'email': request.user.email,
                    'birth_date': request.user.persona.fecha_nacimiento,
                    'avatar': request.user.persona.avatar}
        form_update = UserUpdateForm(data)
        is_active = request.user.is_active
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    if request.method == 'POST':
        form_update = UserUpdateForm(request.POST, request.FILES)
        if form_update.is_valid():
            first_name = form_update.cleaned_data['first_name']
            last_name = form_update.cleaned_data['last_name']
            birth_date = form_update.cleaned_data['birth_date']
            sex = form_update.cleaned_data['sex']
            email = form_update.cleaned_data['email']
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = email
            profile = request.user.persona
            profile.fecha_nacimiento = birth_date
            profile.sexo = sex
            try:
                profile.avatar = request.FILES['avatar']
            except KeyError:
                pass  # print 'Archivo dash/view.edit_account linea 308'
            user.save()
            profile.save()
            messages.append("Se actualizo correctamente el perfil")
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'form_search': searchbox,
        'messages': messages,
        'is_active': is_active},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def edit_pass(request):
    searchbox = SearchBox()
    messages = []
    if request.method == 'POST':
        form_update = PassUpdateForm(user=request.user, data=request.POST or None)
        if form_update.is_valid():
            new_pass = form_update.cleaned_data['new_pass']
            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.append("Se actualizó correctamente la contraseña")
    else:
        form_update = PassUpdateForm(user=request.user)
    return render_to_response('dash/edit_pass.html',
        {'form_update': form_update,
        'form_search': searchbox,
        'messages': messages},
        context_instance=RequestContext(request))


def preguntas_mas_frecuentes(request):
    searchbox = SearchBox()
    form_login = UserLogin()
    return render_to_response('dash/preguntas_mas_frecuentes.html',
        {'form_search': searchbox,
        'form_login': form_login},
        context_instance=RequestContext(request))


def temas_de_ayuda(request):
    searchbox = SearchBox()
    form_login = UserLogin()
    return render_to_response('dash/temas_de_ayuda.html',
        {'form_search': searchbox,
        'form_login': form_login},
        context_instance=RequestContext(request))


def get_cant_mensajes(request):
    return request.user.mensajes_recibidos.filter(
            estado='noleido').count()


@login_required(login_url='/accounts/user/')
def dar_baja_cuenta(request):
    searchbox = SearchBox()
    account = request.user
    account.is_active = False
    account.save()
    messages = ['Tu cuenta ha sido desactivada']
    try:
        data = {'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'sex': request.user.persona.sexo,
                    'email': request.user.email,
                    'birth_date': request.user.persona.fecha_nacimiento,
                    'avatar': request.user.persona.avatar}
        form_update = UserUpdateForm(data)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'form_search': searchbox,
        'messages': messages,
        'is_active': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def activar_cuenta(request):
    searchbox = SearchBox()
    account = request.user
    account.is_active = True
    account.save()
    messages = ['Tu cuenta ha sido activada']
    try:
        data = {'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                    'sex': request.user.persona.sexo,
                    'email': request.user.email,
                    'birth_date': request.user.persona.fecha_nacimiento,
                    'avatar': request.user.persona.avatar}
        form_update = UserUpdateForm(data)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'form_search': searchbox,
        'messages': messages,
        'is_active': True},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def dejar_de_seguir_usuario(request, user_id):
    user_to_follow = User.objects.get(id=user_id)
    my_profile = request.user.persona
    my_profile.following.remove(user_to_follow)
    return HttpResponseRedirect('/dash/follow/{0}'.format(user_id))


@login_required(login_url='/accounts/user/')
def dejar_de_seguir_usuarios(request):
    searchbox = SearchBox()
    notificaciones_noleidas = get_cant_notificaciones(request)
    recomendaciones_noleidas = get_cant_recomendaciones(request)
    mensajes_nolidas = get_cant_mensajes(request)
    if request.method == 'POST':
        my_profile = request.user.persona
        lista_dejar_de_seguir = request.POST.getlist('eliminados')
        for user in lista_dejar_de_seguir:
            user_to_unfollow = User.objects.get(id=user)
            my_profile.following.remove(user_to_unfollow)
        return HttpResponseRedirect('/dash/logbook')
    else:
        return render_to_response('dash/dejar_de_seguir.html',
            {'form_search': searchbox,
            'notificaciones_noleidas': notificaciones_noleidas,
            'recomendaciones_noleidas': recomendaciones_noleidas,
            'mensajes_nolidas': mensajes_nolidas},
            context_instance=RequestContext(request))
