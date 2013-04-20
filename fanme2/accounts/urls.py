from django.conf.urls.defaults import patterns, url
from django.views.generic.base import RedirectView
from accounts import views


urlpatterns = patterns('',
    (r'^$', RedirectView.as_view(url='/accounts/profile/')),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/create/$', views.create_profile, name='create_profile'),
)
