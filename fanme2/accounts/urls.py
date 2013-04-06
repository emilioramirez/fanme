from django.conf.urls.defaults import patterns, url
from django.views.generic.simple import redirect_to
from accounts import views


urlpatterns = patterns('',
    (r'^$', redirect_to, {'url': '/accounts/profile/'}),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/create/$', views.create_profile, name='create_profile'),
)
