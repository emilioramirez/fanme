from django.conf.urls.defaults import patterns
from bussiness import views


urlpatterns = patterns('',
    #(r'^/notificacion/nuevo/$', views.new_notificacion),
    (r'^dash_planes/$', views.dash_planes),
    (r'^elegir_plan/$', views.elegir_plan),
)
