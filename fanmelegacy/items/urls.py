from django.conf.urls.defaults import patterns, url
from items import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    url(r'^item/(?P<item_id>\d+)/$', views.item, name="item-detail"),
    (r'^empresa/(?P<empresa_id>\d+)/$', views.empresa),
    (r'^item/register/$', views.register_item),
    (r'^fan/(?P<item_id>\d+)/$', views.fan),
    (r'^unfan/(?P<item_id>\d+)/$', views.unfan),

    (r'^comment/eliminar/(?P<comment_id>\d+)/$', views.delete_own_comment),
    
    (r'^recomendation/(?P<item_id>\d+)/$', views.recomendation),
    (r'^denunciar_item/(?P<item_id>\d+)/$', views.denunciar_item),
)
