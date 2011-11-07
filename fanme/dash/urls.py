from django.conf.urls.defaults import patterns
from fanme.dash import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    (r'^dashboard/$', views.dashboard),
    (r'^dashboard/(?P<topic_id>\d+)$', views.dashboard_topic),
    (r'^following/$', views.following),
    (r'^followers/$', views.followers),
    (r'^logbook/$', views.logbook),
    (r'^logbook/(?P<user_id>\d+)$', views.logbook_user),
    (r'^topicos/$', views.topicos),
    (r'^results/$', views.results),
    (r'^empresa/$', views.empresa),
    (r'^fans/', views.my_fans_items),
    (r'^comments/$', views.my_comments_items),
    (r'^recomendated/$', views.recomendaciones_enviadas),
    (r'^recomendation/$', views.recomendaciones_recibidas),
    (r'^follow/(?P<user_id>\d+)$', views.follow_user),
    (r'^follow/request/(?P<user_id>\d+)$', views.follow_request),
    (r'^edit_account/$', views.edit_account),
    (r'^edit_pass/$', views.edit_pass),
)
