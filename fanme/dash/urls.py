from django.conf.urls.defaults import patterns
from fanme.dash import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    (r'^dashboard/$', views.dashboard),
    (r'^logbook/$', views.logbook),
    (r'^topicos/$', views.topicos),
    (r'^results/$', views.results),
    (r'^empresa/$', views.empresa),
    (r'^follow/(?P<user_id>\d+)$', views.follow_user),
    (r'^fans/', views.my_fans_items),
    (r'^logbook/(?P<user_id>\d+)$', views.logbook_user),
    (r'^follow/request/(?P<user_id>\d+)$', views.follow_request),
    (r'^following/$', views.following),
    (r'^followers/$', views.followers),
)
