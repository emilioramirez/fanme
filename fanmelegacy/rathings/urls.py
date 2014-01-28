from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'^like/add/(?P<object_id>\d+)/$', 'rathings.views.like'),
    url(r'^dislike/add/(?P<object_id>\d+)/$', 'rathings.views.dislike'),
)