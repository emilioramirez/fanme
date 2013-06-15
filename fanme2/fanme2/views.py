from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def home(request):
    context = {}
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        print(username, password)
        user = authenticate(username=username, password=password)
        print user
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('accounts/profile')
            #else:
                # Return a disabled account error message
        else:
            return HttpResponseRedirect('/accounts/login')
    else:
        form = AuthenticationForm(request)
        context = {'form': form}
        return render_to_response('base_menu_home.html', context,
            context_instance=RequestContext(request))


@login_required
def dashboard(request):
    items = ['El Principito', 'Game Of Thrones', 'How I Met Your Mother', 'Restaurante FanME']
#    context = {}
    return render_to_response('dashboard.html', {'recomended_items': items},
            context_instance=RequestContext(request))


@login_required
def item(request):
    return render_to_response('item.html',
            context_instance=RequestContext(request))
