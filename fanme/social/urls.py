from django.conf.urls.defaults import patterns
from fanme.social import views


urlpatterns = patterns('',
    (r'^eventos/$', views.eventos),
    (r'^nuevo/$', views.new_evento),
)
