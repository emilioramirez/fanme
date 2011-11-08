from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from fanme.dash.forms import SearchBox, UserUpdateForm, PassUpdateForm
from fanme.items.models import Item
from fanme.accounts.models import Persona, Empresa
from fanme.segmentation.models import Topico
from fanme.items.models import Recomendacion
from django.db.models import Q
from django import forms
from fanme import recommendations
from fanme.accounts.forms import UserLogin


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
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/dashboard.html', {'form_search': searchbox,
        'topicos': items_by_topics, 'r_topics': root_topics},
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
    messages = ['Estos usuarios se han hecho fan']
    return render_to_response('dash/empresa.html', {'form_search': searchbox,
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
    except Persona.DoesNotExist:
        return HttpResponseRedirect('/dash/empresa/')
    return render_to_response('dash/mis_recomendaciones_recibidas.html',
        {'form_search': searchbox, 'messages': messages,
        'recomendaciones': items,
            'is_fan': False},
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
        'messages': messages},
        context_instance=RequestContext(request))


@login_required(login_url='/accounts/user/')
def edit_pass(request):
    searchbox = SearchBox()
    messages = []
    if request.method == 'POST':
        form_update = PassUpdateForm(request.POST)
        if form_update.is_valid():
            actual_pass = form_update.cleaned_data['actual_pass']
            new_pass = form_update.cleaned_data['new_pass']
            if not request.user.check_password(actual_pass):
                raise forms.ValidationError("La contrasenia no coincide")
            user = request.user
            user.password = new_pass
            user.save()
            messages.append("Se actualizo correctamente la contrasenia")
    else:
        form_update = PassUpdateForm()
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
