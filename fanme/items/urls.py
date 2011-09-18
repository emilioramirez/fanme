from django.conf.urls.defaults import patterns
from fanme.items import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    (r'^item/(?P<item_id>\d+)$', views.item),
    (r'^empresa/(?P<empresa_id>\d+)$', views.empresa),
    (r'^register_item/', views.register_item),
    (r'^fan/(?P<item_id>\d+)$', views.fan),
    (r'^unfan/(?P<item_id>\d+)$', views.unfan),
)
