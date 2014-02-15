from django.conf.urls.defaults import patterns, url
from bussiness import views


urlpatterns = patterns('',
    #(r'^/notificacion/nuevo/$', views.new_notificacion),
    url(r'^dash_empresa/$', views.dash_empresa, name="dash_empresa"),
    url(r'^dash_planes/$', views.dash_planes, name="dash_planes"),
    (r'^elegir_plan/$', views.elegir_plan),
    (r'^registrar_enlace/(?P<item_id>\d+)$', views.registrar_enlace),
    url(r'^pago_plan/$', views.pago_plan, name="pago_plan"),
)
