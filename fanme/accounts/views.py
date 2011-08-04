# Views
from django.http import HttpResponseRedirect
from django import forms
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from fanme.accounts.forms import UserRegisterForm, CompanyRegisterForm, UserLogin
from fanme.accounts.models import Persona, Empresa
from fanme.support.models import Rubro


def register_user(request):
    if request.method == 'POST': # If the form has been submitted...
        form_register = UserRegisterForm(request.POST) # A form bound to the POST data
        if form_register.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            #~ username = form_register.cleaned_data['username']
            first_name = form_register.cleaned_data['first_name']
            last_name = form_register.cleaned_data['last_name']
            birth_date = form_register.cleaned_data['birth_date']
            sex = form_register.cleaned_data['sex']
            email = form_register.cleaned_data['email']
            password = form_register.cleaned_data['password']
            user = User.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            profile = Persona()
            profile.user = user
            profile.fecha_nacimiento = birth_date
            profile.sexo = sex
            user.save()
            profile.save()
            return HttpResponseRedirect('/accounts/thanks/') # Redirect after POST
        #~ elif form_login.is_valid(): # All validation rules pass
            #~ return HttpResponseRedirect('/dashboard/') # Redirect after POST
    else:
        form_register = UserRegisterForm() # An unbound form
    form_login = UserLogin() # An unbound form
    return render_to_response('accounts/register_user_form.html',
                            {'form_register': form_register, 'form_login': form_login },
                            context_instance=RequestContext(request))

def register_company(request):
    if request.method == 'POST': # If the form has been submitted...
        form_register = CompanyRegisterForm(request.POST) # A form bound to the POST data
        if form_register.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            username = form_register.cleaned_data['email']
            razon_social = form_register.cleaned_data['razon_social']
            direccion = form_register.cleaned_data['direccion']
            rubro = form_register.cleaned_data['rubro']
            url = form_register.cleaned_data['url']
            email = form_register.cleaned_data['email']
            password = form_register.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            profile = Empresa()
            profile.user = user
            profile.razon_social = razon_social
            profile.site = url
            user.save()
            profile.save()
            profile.rubros.add(Rubro.objects.get(nombre=rubro))
            profile.save()
            return HttpResponseRedirect('/accounts/thanks/') # Redirect after POST
    else:
        form_register = CompanyRegisterForm() # An unbound form
    form_login = UserLogin() # An unbound form
    return render_to_response('accounts/register_company_form.html',
                             {'form': form_register, 'form_login': form_login },
                              context_instance=RequestContext(request))

def login_user(request):
    if request.method == 'POST': # If the form has been submitted...
        form_login = UserLogin(request.POST) # A form bound to the POST data
        if form_login.is_valid(): # All validation rules pass
            post_user = form_login.cleaned_data['login_username']
            post_pass = form_login.cleaned_data['login_password']
            user = authenticate(username=post_user, password=post_pass)
            login(request, user)
            return HttpResponseRedirect('/dash/dashboard/') # Redirect after POST
    else:
        form_login = UserLogin() # An unbound form
    form_register = UserRegisterForm() # An unbound form
    return render_to_response('accounts/register_user_form.html',
                            {'form_register': form_register, 'form_login': form_login },
                            context_instance=RequestContext(request))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/accounts/user/')


def thanks(request):
    form_login = UserLogin() # A form bound to the POST data
    return render_to_response('accounts/thanks.html',
                             {'form_login': form_login })
                             

def topicsChoisses(request):
    form_login = UserLogin() # A form bound to the POST data

    return render_to_response('accounts/topicsChoisses.html',
                             {'form_login': form_login }) 
