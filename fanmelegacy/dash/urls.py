from django.conf.urls.defaults import patterns, url
from dash import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    (r'^dashboard/(?P<topic_id>\d+)$', views.dashboard_topic),
    (r'^dashboard/topic/add/(?P<topic_id>\d+)$', views.dashboard_topic_add),
    (r'^dashboard/all$', views.dashboard_all),
    (r'^following/$', views.following),
    (r'^followers/$', views.followers),
    url(r'^logbook/$', views.logbook, name="logbook"),
    (r'^logbook/(?P<user_id>\d+)$', views.logbook_user),
    url(r'^topicos/$', views.topicos, name="topicos"),
    url(r'^results/$', views.results, name="results"),
    (r'^empresa/$', views.empresa),
    (r'^fans/', views.my_fans_items),
    (r'^comments/$', views.my_comments_items),
    (r'^recomendated/$', views.recomendaciones_enviadas),
    (r'^recomendation/$', views.recomendaciones_recibidas),
    (r'^follow/(?P<user_id>\d+)$', views.follow_user),
    (r'^follow/request/(?P<user_id>\d+)$', views.follow_request),
    url(r'^edit_account/$', views.edit_account, name="edit_account"),
    (r'^edit_pass/$', views.edit_pass),
    (r'^preguntas_mas_frecuentes/$', views.preguntas_mas_frecuentes),
    (r'^temas_de_ayuda/$', views.temas_de_ayuda),
    (r'^dar_baja_cuenta', views.dar_baja_cuenta),
    (r'^activar_cuenta', views.activar_cuenta),
    (r'^unfollow/(?P<user_id>\d+)$', views.dejar_de_seguir_usuario),
    (r'^dejar_de_seguir', views.dejar_de_seguir_usuarios),
    (r'^dashboard_ayuda', views.dashboard_ayuda),
    (r'^logbook_ayuda', views.logbook_ayuda),
)
