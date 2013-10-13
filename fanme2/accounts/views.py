from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.forms import ProfileUserForm


@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('create_profile'))
    context = {'profile': profile, 'page_title': 'Perfil de usuario'}
    return render_to_response('base_menu_profile.html', context,
                              context_instance=RequestContext(request))


@login_required
def create_profile_common(request):
    """
    Create a form for user profile
    """
    try:
        # The user has a profile, redirect to profile
        profile = request.user.profile
        return HttpResponseRedirect(reverse('profile'))
    except Profile.DoesNotExist:
        print "No existe el usuario, accounts/view/create_profile_common"
    if request.method == 'POST':
        profile_user_form = ProfileUserForm(request.POST)
        if profile_user_form.is_valid():
            profile_user = profile_user_form.save(commit=False)
            profile_user.user = request.user
            profile_user.first_login = True
            profile_user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        profile_user_form = ProfileUserForm()
    page_title = u"Crear su perfil"
    return render_to_response('base_menu_profile_create.html', locals(),
                              context_instance=RequestContext(request))
