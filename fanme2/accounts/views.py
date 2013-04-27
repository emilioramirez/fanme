from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from accounts.forms import ProfileForm



@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return HttpResponseRedirect(reverse('create_profile'))
    context = {'profile': 'Exite el perfil', 'p': profile}
    return render_to_response('base_menu_profile.html', context,
                              context_instance=RequestContext(request))


@login_required
def create_profile(request):
    """
    Create a form for user profile
    """
    profile_form = ProfileForm()
    page_title = u"Crear su perfil"
    return render_to_response('base_menu_profile_create.html', locals(),
                              context_instance=RequestContext(request))
