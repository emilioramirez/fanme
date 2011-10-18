from django.conf.urls.defaults import patterns
from fanme.social import views


urlpatterns = patterns('',
    (r'^messages/$', views.messages),
    (r'^new_message/$', views.new_message),
    (r'^messages_user/(?P<user_id>\d+)$', views.messages_user),
    (r'^company_query/(?P<company_id>\d+)$', views.company_query),
    (r'^eventos/$', views.eventos),
    (r'^nuevo/$', views.new_evento),
    (r'^evento/(?P<evento_id>\d+)$', views.evento),
    (r'^evento/edit/(?P<evento_id>\d+)$', views.edit_evento),
    (r'^evento/delete/(?P<evento_id>\d+)$', views.delete_evento),
)
