from django.conf.urls.defaults import patterns
from fanme.social import views


urlpatterns = patterns('',
    (r'^/notificacion/nuevo/$', views.new_notificacion),
)
