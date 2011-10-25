from django.conf.urls.defaults import patterns
from fanme.social import views


urlpatterns = patterns('',
    (r'^messages/$', views.messages),
    (r'^new_message/$', views.new_message),
    (r'^messages_user/(?P<user_id>\d+)$', views.messages_user),
    (r'^company_query/(?P<company_id>\d+)$', views.company_query),
    (r'^eventos/$', views.eventos),
    (r'^notificaciones/$', views.notificaciones),
    (r'^notificacion/delete/(?P<notificacion_id>\d+)$',
        views.delete_notificacion),
    (r'^nuevo/$', views.new_evento),
    (r'^evento/(?P<evento_id>\d+)$', views.evento),
    (r'^evento/edit/(?P<evento_id>\d+)$', views.edit_evento),
    (r'^evento/delete/(?P<evento_id>\d+)$', views.delete_evento),
    (r'^company_messages/$', views.company_messages),
    (r'^company_response_message/(?P<user_id>\d+)$',
        views.company_response_message),
    (r'^new_notification/$', views.new_notification),
    (r'^user_main_notification/$', views.user_main_view_notifications),
    (r'^notifications_by_company/(?P<company_id>\d+)$',
        views.notification_by_company),
)
