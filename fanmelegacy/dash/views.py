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
from django.contrib import messages

from dash.forms import SearchBox, UserUpdateForm, PassUpdateForm
from items.models import Item
from accounts.models import Persona, Empresa
from segmentation.models import Topico
from items.models import Recomendacion, Comentario
from fanmelegacy import recommendations
from accounts.forms import UserLogin
from itertools import chain
from operator import attrgetter
from django.contrib.auth import logout
from social.models import Actividad
import datetime


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
                lista = Item.objects.filter(nombre=itemname).filter(
                    topico__in=my_profile.topicos.all())
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


#@login_required(login_url='/accounts/user/')
#def dashboard_topic(request, topic_id):
#    searchbox = SearchBox()
#    lista = []
#    try:
#        #block recommendation
#        recommendations.diccionario = recommendations.getMatrix()
#        ranking = recommendations.getRecommendations(
#            recommendations.diccionario, request.user.username)
#        #block recommendation
#        root_topics = Topico.objects.filter(padre=None)
#        topico = Topico.objects.get(id=topic_id)
#        yes = request.user.persona.topicos.get(id=topic_id)
##        if yes:
##            lista.append(Item.objects.filter(topico__exact=topico).order_by(
##                '-cantidad_fans'))
#        if yes:
#            if ranking != []:
#                for rank, itemname in ranking:
#                    lista.append(Item.objects.filter(nombre=itemname,
#                        topico__exact=topico).order_by('-cantidad_fans'))
#            else:
#                lista.append(Item.objects.filter(topico__exact=topico).order_by(
#                '-cantidad_fans'))
#
#    except Persona.DoesNotExist:
#        return HttpResponseRedirect('/dash/empresa/')
#    except Topico.DoesNotExist:
#        return render_to_response('dash/dashboard.html',
#            {'form_search': searchbox, 'topicos': lista,
#                'r_topics': root_topics},
#            context_instance=RequestContext(request))
#    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
#        'topicos': lista, 'r_topics': root_topics},
#        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def dashboard_topic(request, topic_id):
    try:
        top = Topico.objects.get(id=topic_id)
        profile = request.user.persona
        profile.topicos.remove(top)
        profile.save()
    except Topico.DoesNotExist:
        pass
    except Persona.DoesNotExist:
        pass
    return HttpResponseRedirect('/dash/dashboard/')


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
def dashboard_all(request):
    searchbox = SearchBox()
    root_topics = Topico.objects.filter(padre=None)
    profile = request.user.persona
    items_by_topics = []
    if set(profile.topicos.all()) == set(root_topics):
        profile.topicos = []
        profile.save()
        all_topics = False
    else:
        try:
            profile.topicos = root_topics
            profile.save()
            all_topics = True
            lista = Item.objects.all().order_by('-cantidad_fans')
            items_by_topics.append(lista)
        except Topico.DoesNotExist:
            pass
        except Persona.DoesNotExist:
            pass
    notificaciones_noleidas = get_cant_notificaciones(request)
    recomendaciones_noleidas = get_cant_recomendaciones(request)
    mensajes_nolidas = get_cant_mensajes(request)
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'all_topics': all_topics, 'r_topics': root_topics,
        'topicos': items_by_topics,
        'notificaciones_noleidas': notificaciones_noleidas,
        'recomendaciones_noleidas': recomendaciones_noleidas,
        'mensajes_nolidas': mensajes_nolidas},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook(request):
    searchbox = SearchBox()
    try:
        followings = request.user.persona.following.all()
        active_followings = followings.filter(is_active=True)
        actividades = []
        for user in active_followings:
            actividades = sorted(
                chain(
                    user.act_origen.all(), actividades),
                key=attrgetter('fecha'), reverse=True)
        notificaciones_noleidas = get_cant_notificaciones(request)
        recomendaciones_noleidas = get_cant_recomendaciones(request)
        mensajes_nolidas = get_cant_mensajes(request)
        cant_following = active_followings.count()
        cant_followers = get_active_followers(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/logbook.html', {'form_search': searchbox,
        'notificaciones_noleidas': notificaciones_noleidas,
        'recomendaciones_noleidas': recomendaciones_noleidas,
        'mensajes_nolidas':mensajes_nolidas, 'cant_following': cant_following,
        'actividades': actividades, 'cant_followers': cant_followers},
        context_instance=RequestContext(request))


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
    messages.add_message(request, message.INFO, 'Estos usuarios se han hecho fan')
    return render_to_response('bussiness/dash_empresa.html', {'form_search': searchbox},
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
        if not my_profile.following.filter(id=user_logbook.id):
            return HttpResponseRedirect('/dash/follow/{0}'.format(user_id))
        else:
            actividades = []
            actividades = sorted(
                chain(
                    user_logbook.act_origen.all(), actividades),
                key=attrgetter('fecha'), reverse=True)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/logbook_user.html',
        {'form_search': searchbox, 'user_logbook': user_logbook,
        'actividades': actividades},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_fans_items(request):
    searchbox = SearchBox()
    lista = []
    try:
        items = request.user.persona.items.all()
        for item in items:
            lista.append(
                (item, 0)
            )
        messages.add_message(request, messages.INFO, "Sos fan de")
    except Persona.DoesNotExist:
            return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mi_fanes.html',
        {'form_search': searchbox, 'items': lista, 'is_fan': True},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_comments_items(request):
    searchbox = SearchBox()
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
        messages.add_message(request, messages.INFO, "Has comentado los siguientes items")
    except Persona.DoesNotExist:
            return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mis_comentarios.html',
        {'form_search': searchbox, 'items': lista, 'is_fan': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendaciones_enviadas(request):
    searchbox = SearchBox()
    try:
        request.user.persona
        items_ids = request.user.recomendaciones_enviadas.all().values_list(
            'item', flat=True).distinct()
        items = Item.objects.filter(id__in=items_ids)
        messages.add_message(request, messages.INFO, "Has recomendado los siguientes items")
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    recomendaciones = request.user.recomendaciones_enviadas.all().order_by(
        'fecha')
    return render_to_response('dash/mis_recomendaciones_enviadas.html',
        {'form_search': searchbox,
        'recomendaciones': items,
            'is_fan': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendaciones_recibidas(request):
    searchbox = SearchBox()
    try:
        request.user.persona
        items_ids = request.user.recomendaciones_recibidas.all().values_list(
            'item', flat=True).distinct().filter(user_origen__is_active=True)
        items = Item.objects.filter(id__in=items_ids)
        rec = request.user.recomendaciones_recibidas.filter(estado="noleido")
        for r in rec:
            r.estado = "leido"
            r.save()
            messages.add_message(request, messages.INFO, "Te han recomendado los siguientes items")
        notificaciones_noleidas = get_cant_notificaciones(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mis_recomendaciones_recibidas.html',
        {'form_search': searchbox,
        'recomendaciones': items,
        'notificaciones_noleidas': notificaciones_noleidas, 'is_fan': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def following(request):
    searchbox = SearchBox()
    messages.add_message(request, messages.INFO, 'Estas siguiendo a estos usuarios')
    followings = request.user.persona.following.all()
    active_followings = followings.filter(is_active=True)
    cant_following = active_followings.count()
    cant_followers = get_active_followers(request)
    return render_to_response('dash/following.html',
        {'form_search': searchbox,
         'active_followings': active_followings,
         'cant_following': cant_following,
         'cant_followers': cant_followers},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def followers(request):
    searchbox = SearchBox()
    messages.add_message(request, messages.INFO, 'Estos usuarios te estan siguiendo')
    cant_followers = get_active_followers(request)
    cant_following = get_active_followings(request)
    return render_to_response('dash/followers.html',
        {'form_search': searchbox,
        'cant_followers': cant_followers,
        'cant_following': cant_following},
        context_instance=RequestContext(request))


def get_active_followings(request):
    followings = request.user.persona.following.all()
    active_followings = followings.filter(is_active=True)
    return active_followings.count()


def get_active_followers(request):
    followers = request.user.followers
    return followers.count()


@login_required(login_url='/accounts/user/')
def edit_account(request):
    searchbox = SearchBox()
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
            messages.add_message(request, messages.SUCCESS, "Se actualizo correctamente el perfil")
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'form_search': searchbox, 'is_active': is_active},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def edit_pass(request):
    searchbox = SearchBox()
    if request.method == 'POST':
        form_update = PassUpdateForm(user=request.user, data=request.POST or None)
        if form_update.is_valid():
            new_pass = form_update.cleaned_data['new_pass']
            user = request.user
            user.set_password(new_pass)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Se actualizó correctamente la contraseña")
    else:
        form_update = PassUpdateForm(user=request.user)
    return render_to_response('dash/edit_pass.html',
        {'form_update': form_update,
        'form_search': searchbox},
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
    messages.add_message(request, messages.WARNING, 'Tu cuenta ha sido desactivada')
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
        'is_active': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def activar_cuenta(request):
    searchbox = SearchBox()
    account = request.user
    account.is_active = True
    account.save()
    messages.add_message(request, messages.SUCCESS, 'Tu cuenta ha sido activada')
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
    followings = request.user.persona.following.all()
    active_followings = followings.filter(is_active=True)
    cant_following = active_followings.count()
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
            'mensajes_nolidas': mensajes_nolidas,
            'active_followings': active_followings,
            'cant_following': cant_following},
            context_instance=RequestContext(request))


def dashboard_ayuda(request):
    user = request.user
    searchbox = None
    if user.is_authenticated():
        searchbox = SearchBox()
    try:
        root_topics = Topico.objects.filter(padre=None)
        item = Item.objects.get(pk=1)
        form_login = UserLogin()
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/dashboard_ayuda.html', {
        'item': item, 'r_topics': root_topics,
        'form_login': form_login,
        'form_search': searchbox},
        context_instance=RequestContext(request))


def logbook_ayuda(request):
    user = request.user
    searchbox = None
    actividades = []
    user = User()
    #Creo el usuario
    user.first_name = 'Gabriel'
    user.last_name = 'Arcos'
    actividad = Actividad()
    #Creo la primer actividad
    actividad.item = Item.objects.get(pk=1)
    actividad.usuario_origen = user
    actividad.tipo = "fan"
    actividad.fecha = datetime.datetime.now()
    actividad.descripcion = "se hizo fan de"
    actividades.append(actividad)
    #Creo la segunda actividad
    comentario = Comentario()
    comentario.comentario = "Muy buena peli!"
    actividad = Actividad()
    actividad.item = Item.objects.get(pk=2)
    actividad.usuario_origen = user
    actividad.tipo = "comentario"
    actividad.fecha = datetime.datetime.now()
    actividad.descripcion = "realizo un comentario en"
    actividad.comentario = comentario
    actividades.append(actividad)
    #Creo la tercer actividad
    actividad = Actividad()
    actividad.item = Item.objects.get(pk=2)
    actividad.usuario_origen = user
    actividad.tipo = "recomendacion"
    actividad.fecha = datetime.datetime.now()
    actividad.descripcion = "recomendado el siguiente item"
    actividad.comentario = comentario
    actividades.append(actividad)
    if user.is_authenticated():
        searchbox = SearchBox()
    try:
        item = Item.objects.get(pk=1)
        form_login = UserLogin()
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/logbook_ayuda.html', {
        'item': item,
        'form_login': form_login,
        'form_search': searchbox,
        'actividades': actividades},
        context_instance=RequestContext(request))

