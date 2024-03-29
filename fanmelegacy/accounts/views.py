from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.core.urlresolvers import reverse

from registration.models import RegistrationProfile

from accounts.forms import UserRegisterForm, CompanyRegisterForm
from accounts.forms import UserLogin
from accounts.models import Persona, Empresa
from support.models import Rubro
from segmentation.models import Topico


def register_user(request):
    if request.method == 'POST':
        form_register = UserRegisterForm(request.POST)
        if form_register.is_valid():
            first_name = form_register.cleaned_data['first_name']
            last_name = form_register.cleaned_data['last_name']
            birth_date = form_register.cleaned_data['birth_date']
            sex = form_register.cleaned_data['sex']
            email = form_register.cleaned_data['email']
            password = form_register.cleaned_data['password']
            # Create a inactive user with django-registration
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            user = RegistrationProfile.objects.create_inactive_user(email, email,
                                                                        password, site)
            user.first_name = first_name
            user.last_name = last_name
            profile = Persona()
            profile.user = user
            profile.fecha_nacimiento = birth_date
            profile.sexo = sex
            profile.is_first_time = True
            user.save()
            profile.save()
            return HttpResponseRedirect('/accounts/thanks/')
        #~ elif form_login.is_valid(): # All validation rules pass
            #~ return HttpResponseRedirect('/dashboard/') # Redirect after POST
    else:
        form_register = UserRegisterForm()
    form_login = UserLogin()
    return render_to_response('accounts/register_user_form.html',
        {'form_register': form_register, 'form_login': form_login},
        context_instance=RequestContext(request))


def register_company(request):
    if request.method == 'POST':
        form_register = CompanyRegisterForm(request.POST)
        if form_register.is_valid():
            username = form_register.cleaned_data['email']
            razon_social = form_register.cleaned_data['razon_social']
            direccion = form_register.cleaned_data['direccion']
            rubro = form_register.cleaned_data['rubro']
            url = form_register.cleaned_data['url']
            email = form_register.cleaned_data['email']
            password = form_register.cleaned_data['password']
            # Create a inactive user with django-registration
            if Site._meta.installed:
                site = Site.objects.get_current()
            else:
                site = RequestSite(request)
            user = RegistrationProfile.objects.create_inactive_user(username, email,
                                                                        password, site)
            profile = Empresa()
            profile.user = user
            profile.razon_social = razon_social
            profile.direccion = direccion
            profile.site = url
            profile.is_first_time = True
            user.save()
            profile.save()
            profile.rubros.add(Rubro.objects.get(nombre=rubro))
            profile.save()
            return HttpResponseRedirect('/accounts/thanks/')
    else:
        form_register = CompanyRegisterForm()
    form_login = UserLogin()
    return render_to_response('accounts/register_company_form.html',
        {'form': form_register, 'form_login': form_login},
        context_instance=RequestContext(request))


def login_user(request):
    if request.method == 'POST':
        form_login = UserLogin(request.POST)
        if form_login.is_valid():
            post_user = form_login.cleaned_data['login_username']
            post_pass = form_login.cleaned_data['login_password']
            user = authenticate(username=post_user, password=post_pass)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        profile = request.user.persona
                        if profile.is_first_time:
                            return HttpResponseRedirect('/accounts/topics/')
                        else:
                            return HttpResponseRedirect('/dash/dashboard/')
                    except Persona.DoesNotExist:
                        return HttpResponseRedirect('/bussiness/dash_empresa/')
                else:
                    pass
            else:
                pass
    else:
        form_login = UserLogin()
    form_register = UserRegisterForm()
    return render_to_response('accounts/register_user_form.html',
        {'form_register': form_register, 'form_login': form_login},
        context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/accounts/user/')


def thanks(request):
    form_login = UserLogin()
    return render_to_response('accounts/thanks.html',
        {'form_login': form_login}, context_instance=RequestContext(request))


def my_topics(request):
    if request.method == 'POST':
        topicos = request.POST.getlist('listaSeleccionados')
        user = User.objects.get(id=request.user.id)
        try:
            profile = user.persona
            for topico in topicos:
                top = Topico.objects.get(nombre=topico)
                profile.topicos.add(top)
            profile.is_first_time = False
            profile.save()
            return HttpResponseRedirect('/dash/dashboard/')
        except Persona.DoesNotExist:
                return HttpResponseRedirect(reverse("dash_empresa"))
    return render_to_response('accounts/my_topics.html',
        context_instance=RequestContext(request))
