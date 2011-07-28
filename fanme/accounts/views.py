# Views
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
#from django.contrib.auth.forms import AuthenticationForm
from fanme.accounts.forms import UserRegisterForm, CompanyRegisterForm, UserLogin
from fanme.accounts.models import Persona, Empresa
from fanme.soport.models import Rubro


def register_user(request):
    if request.method == 'POST': # If the form has been submitted...
        form_register = UserRegisterForm(request.POST) # A form bound to the POST data
        form_login = UserLogin(request.POST) # A form bound to the POST data
        if form_register.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            username = form_register.cleaned_data['username']
            birth_date = form_register.cleaned_data['birth_date']
            sex = form_register.cleaned_data['sex']
            email = form_register.cleaned_data['email']
            password = form_register.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            profile = Persona()
            profile.user = user
            profile.fecha_nacimiento = birth_date
            profile.sexo = sex
            user.save()
            profile.save()
            return HttpResponseRedirect('/thanks/') # Redirect after POST
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
        form_login = UserLogin(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            username = form_register.cleaned_data['username']
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
            profile.rubro.add(Rubro.objects.get(nombre=rubro))
            profile.save()
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = CompanyRegisterForm() # An unbound form
        form_login = UserLogin() # An unbound form

    return render_to_response('accounts/register_company_form.html',
                             {'form': form, 'form_login': form_login },
                              context_instance=RequestContext(request))

def login_user(request):
    username = request.POST['login_username']
    password = request.POST['login_password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect('/dashboard/') # Redirect after POST
        else:
            # Return a 'disabled account' error message
            return HttpResponseRedirect('/disable/')
    else:
        # Return an 'invalid login' error message.
        return HttpResponseRedirect('/error/')

def thanks(request):
	form_login = UserLogin(request.POST) # A form bound to the POST data
	
	return render_to_response('accounts/thanks.html',
							 {'form_login': form_login })
