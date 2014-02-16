from django.conf.urls.defaults import patterns, url
from social import views


urlpatterns = patterns('',
    url(r'^mensajes/$', views.mensajes, name="social-mensajes"),
    (r'^company_messages/$', views.company_messages),
    (r'^company_response_message/(?P<user_id>\d+)$', views.company_response_message),
    (r'^consulta_a_empresa/(?P<company_id>\d+)$', views.company_query),
    (r'^evento/(?P<evento_id>\d+)$', views.evento),
    (r'^evento/cancelar/(?P<evento_id>\d+)$', views.cancelar_evento),
    (r'^evento/delete/(?P<evento_id>\d+)$', views.delete_evento),
    (r'^evento/edit/(?P<evento_id>\d+)$', views.edit_evento),
    (r'^evento_ayuda/$', views.evento_ayuda),
    (r'^eventos/$', views.eventos),
    (r'^eventos_ayuda/$', views.eventos_ayuda),
    (r'^messages_ayuda/$', views.messages_ayuda),
    (r'^messages_user/(?P<user_id>\d+)$', views.messages_user),
    (r'^messages_user_ayuda/$', views.messages_user_ayuda),
    (r'^new_message/$', views.new_message),
    (r'^new_notification/$', views.new_notification),
    (r'^notificacion/delete/(?P<notificacion_id>\d+)$', views.delete_notificacion),
    (r'^notificacion/edit/(?P<notificacion_id>\d+)$', views.edit_notificacion),
    (r'^notificaciones/$', views.notificaciones),
    (r'^notificaciones/(?P<notificacion_id>\d+)$', views.notificacion),
    (r'^notifications_by_company/(?P<company_id>\d+)$', views.notification_by_company),
    (r'^nuevo/$', views.new_evento),
    (r'^user_main_notification/$', views.user_main_view_notifications),
    (r'^ver_consulta_item_usuario/(?P<item_id>\d+)/(?P<user_id>\d+)$', views.ver_consultas_item_usuario),
    (r'^ver_consultas/$', views.ver_consultas),
    (r'^ver_consultas_item/(?P<item_id>\d+)$', views.ver_consultas_item),
    (r'^ver_notificaciones/(?P<notificacion_id>\d+)$', views.ver_notificacion),
    (r'^responder_consulta_item/(?P<item_id>\d+)/(?P<user_id>\d+)$', views.responder_consulta),
    (r'^consultas/$', views.consultas_usuario),
    (r'^consulta_empresa/(?P<user_id>\d+)$', views.consultas_usuario_empresas),
    (r'^consulta_empresa/(?P<user_id>\d+)/(?P<item_id>\d+)$', views.consultas_empresa_item),
)
