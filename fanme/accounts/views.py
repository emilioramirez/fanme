# Views
from django.shortcuts import render_to_response
#from django.core.context_processors import csrf
from django.template import RequestContext
from fanme.accounts.forms import UserRegisterForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from fanme.accounts.models import Persona


def dashboard(request):
    return render_to_response('base.html', context_instance=RequestContext(request))


def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserRegisterForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            username = form.cleaned_data['username']
            birth_date = form.cleaned_data['birth_date']
            sex = form.cleaned_data['sex']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username, email, password)
            profile = Persona()
            profile.user = user
            profile.fecha_nacimiento = birth_date
            profile.sexo = sex
            user.save()
            profile.save()
            return HttpResponseRedirect('/dashboard/') # Redirect after POST
    else:
        form = UserRegisterForm() # An unbound form

    return render_to_response('accounts/register_form.html', {'form': form, },
                              context_instance=RequestContext(request))

