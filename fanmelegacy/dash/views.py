# -*- encoding: utf-8 -*-
import datetime
import operator
from operator import attrgetter
from itertools import chain

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse

from accounts.forms import UserLogin
from accounts.models import Persona, Empresa
from dash.forms import SearchBox, UserUpdateForm, PassUpdateForm, EmpresaUpdateForm
from fanmelegacy import recommendations
from items.models import Item, Comentario
from segmentation.models import Topico
from social.models import Actividad

@login_required(login_url='/accounts/user/')
def dashboard(request):
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
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/dashboard.html', {'topicos': items_by_topics,
        'r_topics': root_topics},
        context_instance=RequestContext(request))


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
    return render_to_response('dash/dashboard.html', {'all_topics': all_topics,
        'r_topics': root_topics,
        'topicos': items_by_topics,
        },
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook(request):
    try:
        # mis seguidores activos
        active_followings = request.user.persona.following.filter(is_active=True)
        actividades = []
        # Por cada usuario activo
        for user in active_followings:
            actividades_user = []
            actividad_recomendacion = {}
            # Agrupo las actividades de recomendacion para un item determinado
            for actividad in user.act_origen.filter(tipo='recomendacion'):
                try:
                    actividad_recomendacion[actividad.item].append(actividad)
                except KeyError:
                    actividad_recomendacion[actividad.item] = [actividad]
            # Por item agrego la actividad mas nueva
            for item, acts in actividad_recomendacion.items():
                actividades_user.append(sorted(acts, key=attrgetter('fecha')).pop())
            
            # Actividades totales, mas actividades de recomendacion, mas otras
            actividades = chain(actividades_user, user.act_origen.exclude(tipo='recomendacion'), actividades)
        # Ordeno todo por fecha
        actividades = sorted(actividades, key=attrgetter('fecha'), reverse=True)
        cant_following = active_followings.count()
        cant_followers = get_active_followers(request)
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/logbook.html', {
        'cant_following': cant_following,
        'actividades': actividades, 'cant_followers': cant_followers,
        "breadcrumb": ["Logbook"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def topicos(request):
    return render_to_response('dash/topicos.html', {},
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
    else:
        return render_to_response('dash/results.html',
            {'form_search': searchbox},
            context_instance=RequestContext(request))
    return render_to_response('dash/results.html',
        {'form_search': searchbox,
            'items_result': first_items,
            'users_result': active_users,
            'organizations_result': first_organizations,
            'breadcrumb': ["Resultado de busqueda", search]},
            context_instance=RequestContext(request))


# @login_required(login_url='/accounts/user/')
# def empresa(request):
#     followers = request.user.followers.filter(user__is_active=True)
#     return render_to_response('bussiness/dash_empresa.html',
#         {'followers': followers,
#          'breadcrumb': ["Empresa","Usuarios que te siguen",]},
#         context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def follow_user(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
        my_profile = request.user.persona
        i_follow = my_profile.following.filter(id=user_id)
        if i_follow:
            return HttpResponseRedirect('/dash/logbook/{0}'.format(user_id))
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/follow.html', {'user_to_follow': user_to_follow,
        'breadcrumb': ["Logbook", "{} {}".format(user_to_follow.first_name, (user_to_follow.last_name))]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def follow_request(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise Http404

    try:
        i_follow = request.user.persona.following.filter(pk=user_id)
        if not i_follow:
            request.user.persona.following.add(user_to_follow)
        aux = user_to_follow.persona
        messages.add_message(request, messages.SUCCESS, "Ahora sigues al usuario {}".format(
            user_to_follow.first_name, user_to_follow.last_name))
        return HttpResponseRedirect('/dash/logbook/{0}'.format(user_id))
    except Persona.DoesNotExist:
        messages.add_message(request, messages.SUCCESS, "Ahora sigues a la empresa {}".format(
            user_to_follow.empresa.razon_social))
        return HttpResponseRedirect('/items/empresa/{}/'.format(user_to_follow.pk))
    # return render_to_response('dash/dashboad.html',
    #                                     context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def logbook_user(request, user_id):
    mostrar_boton_dejar_seguir = True
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
        mostrar_boton_dejar_seguir = False
        actividades = []
        actividades = sorted(
            chain(
                user_logbook.act_origen.all(), actividades),
            key=attrgetter('fecha'), reverse=True)
    except User.DoesNotExist:
        messages.add_message(request, messages.WARNING, "El usuario que intentas acceder no existe")
        return HttpResponseRedirect(reverse("dashboad"))
    return render_to_response('dash/logbook_user.html',
        {'user_logbook': user_logbook,
        'actividades': actividades, 'mostrar_boton_dejar_seguir': mostrar_boton_dejar_seguir,
        'breadcrumb': ["Logbook", "{} {}".format(u''.join(user_logbook.first_name).encode('utf-8'),
            u''.join(user_logbook.last_name).encode('utf-8'))]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_fans_items(request):
    try:
        items = request.user.persona.items.all()
    except Persona.DoesNotExist:
            return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/items_stats.html',
        {'items': items, 'is_fan': True, 'breadcrumb': ["Estadisticas",
        "Sos fan de"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def my_comments_items(request):
    try:
        request.user.persona
        comments = request.user.comment_comments.exclude(is_removed=True)
    except Persona.DoesNotExist:
            return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/items_stats_comments.html',
        {'comments': comments, 'is_fan': False, 'breadcrumb': ["Estadisticas",
        "Comentaste"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendaciones_enviadas(request):
    try:
        request.user.persona
        items_ids = request.user.recomendaciones_enviadas.all().values_list(
            'item', flat=True).distinct()
        items = Item.objects.filter(id__in=items_ids)
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/items_stats.html',
        {'items': items,'is_fan': False, "breadcrumb": ["Estadisticas", "Recomendaciones", "Enviadas"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def recomendaciones_recibidas(request):
    try:
        request.user.persona
        items_ids = request.user.recomendaciones_recibidas.all().values_list(
            'item', flat=True).distinct().filter(user_origen__is_active=True)
        items = Item.objects.filter(id__in=items_ids)
        rec = request.user.recomendaciones_recibidas.filter(estado="noleido")
        for r in rec:
            r.estado = "leido"
            r.save()
    except Persona.DoesNotExist:
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/items_stats.html',
        {'items': items, 'breadcrumb': ["Social", "Recomendaciones", "Recibidas"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def following(request):
    followings = request.user.persona.following.all()
    active_followings = followings.filter(is_active=True)
    cant_following = active_followings.count()
    cant_followers = get_active_followers(request)
    return render_to_response('dash/following.html',
        {'active_followings': active_followings,
         'cant_following': cant_following,
         'cant_followers': cant_followers,
         'breadcrumb': ["Social","Usuarios que sigues",]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def followers(request):
    cant_followers = get_active_followers(request)
    cant_following = get_active_followings(request)
    return render_to_response('dash/followers.html',
        {'cant_followers': cant_followers,
        'cant_following': cant_following,
        'breadcrumb': ["Social", "Usuarios que me siguen"]},
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
    form = None
    empresa = False
    try:
        data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'sex': request.user.persona.sexo,
            'email': request.user.email,
            'birth_date': request.user.persona.fecha_nacimiento,
            'avatar': request.user.persona.avatar}
        form_update = UserUpdateForm(initial=data)
        form = UserUpdateForm
    except Persona.DoesNotExist:
        data = {
            'razon_social': request.user.empresa.razon_social,
            'direccion': request.user.empresa.direccion,
            'rubro': [r.pk for r in request.user.empresa.rubros.all()],
            'email': request.user.email,
            'url': request.user.empresa.site}
        form_update = EmpresaUpdateForm(initial=data)
        form = EmpresaUpdateForm
        empresa = True
    if request.method == 'POST':
        form_update = form(request.POST, request.FILES)
        if form_update.is_valid():
            if empresa:
                razon_social = form_update.cleaned_data['razon_social']
                rubros = form_update.cleaned_data['rubro']
                email = form_update.cleaned_data['email']
                url = form_update.cleaned_data['url']
                request.user.empresa.razon_social = razon_social
                request.user.empresa.rubros = rubros
                request.user.empresa.site = url
                request.user.email = email
                request.user.save()
                request.user.empresa.save()
            else:
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
                user.save()
                profile.save()
            messages.add_message(request, messages.SUCCESS, "Se actualizo correctamente el perfil")
            return HttpResponseRedirect("/dash/edit_account/")
    is_active = request.user.is_active
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'is_active': is_active,
        'breadcrumb': ["Datos de la cuenta"]},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def edit_pass(request):
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
        {'form_update': form_update},
        context_instance=RequestContext(request))


def preguntas_mas_frecuentes(request):
    form_login = UserLogin()
    return render_to_response('dash/preguntas_mas_frecuentes.html',
        {'form_login': form_login},
        context_instance=RequestContext(request))


def temas_de_ayuda(request):
    form_login = UserLogin()
    return render_to_response('dash/temas_de_ayuda.html',
        {'form_login': form_login},
        context_instance=RequestContext(request))


def get_cant_mensajes(request):
    return request.user.mensajes_recibidos.filter(
            estado='noleido').count()


@login_required(login_url='/accounts/user/')
def dar_baja_cuenta(request):
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
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'is_active': False},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def activar_cuenta(request):
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
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/edit_account.html',
        {'form_update': form_update,
        'is_active': True},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def dejar_de_seguir_usuario(request, user_id):
    try:
        user_to_follow = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.add_message(request, messages.WARNING, "El usuario que intentas acceder no existe")
        return HttpResponseRedirect(reverse("dashboad"))        
    
    request.user.persona.following.remove(user_to_follow)   
    
    try:
        user_to_follow.persona
        messages.add_message(request, messages.SUCCESS, u"Has dejado de seguir al usuario {0} {1}".format(user_to_follow.first_name, user_to_follow.last_name))
        return HttpResponseRedirect('/dash/follow/{0}'.format(user_to_follow.pk))
    except Persona.DoesNotExist:
        messages.add_message(request, messages.SUCCESS, u"Has dejado de seguir a la empresa {0}".format(user_to_follow.empresa.razon_social))
        return HttpResponseRedirect('/items/empresa/{}/'.format(user_to_follow.pk))




@login_required(login_url='/accounts/user/')
def dejar_de_seguir_usuarios(request):
    active_followings = request.user.persona.following.filter(is_active=True)
    cant_following = active_followings.count()
    cant_followers = get_active_followers(request)
    if request.method == 'POST':
        my_profile = request.user.persona
        lista_dejar_de_seguir = request.POST.getlist('eliminados')
        for user in lista_dejar_de_seguir:
            user_to_unfollow = User.objects.get(id=user)
            my_profile.following.remove(user_to_unfollow)
        return HttpResponseRedirect('/dash/logbook')
    else:
        return render_to_response('dash/dejar_de_seguir.html',
            {'active_followings': active_followings,
            'cant_following': cant_following,
            'cant_followers': cant_followers,
            'breadcrumb': ['Social', "Usuarios que sigues", "Dejar de seguir"]},
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
        return HttpResponseRedirect(reverse("dash_empresa"))
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
        return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('dash/logbook_ayuda.html', {
        'item': item,
        'form_login': form_login,
        'form_search': searchbox,
        'actividades': actividades},
        context_instance=RequestContext(request))


def get_cant_notificaciones(request):
    return request.user.notificaciones_recibidas.filter(
            estado='noleido').count()
