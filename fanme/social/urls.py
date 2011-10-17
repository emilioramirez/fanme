from django.conf.urls.defaults import patterns
from fanme.social import views


urlpatterns = patterns('',
    (r'^eventos/$', views.eventos),
    (r'^nuevo/$', views.new_evento),
    (r'^evento/(?P<evento_id>\d+)$', views.evento),
    (r'^evento/edit/(?P<evento_id>\d+)$', views.edit_evento),
    (r'^evento/delete/(?P<evento_id>\d+)$', views.delete_evento),
)
