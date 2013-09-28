from django.conf.urls.defaults import patterns
from items import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    (r'^item/(?P<item_id>\d+)$', views.item),
    (r'^empresa/(?P<empresa_id>\d+)$', views.empresa),
    (r'^item/register/', views.register_item),
    (r'^fan/(?P<item_id>\d+)$', views.fan),
    (r'^unfan/(?P<item_id>\d+)$', views.unfan),
    (r'^comment/(?P<item_id>\d+)$', views.comment),
    (r'^comment/megusta/(?P<comentario_id>\d+)$', views.me_gusta_comentario),
    (r'^comment/denunciar/(?P<comentario_id>\d+)$', views.denunciar_comentario),
    (r'^recomendation/(?P<item_id>\d+)$', views.recomendation),
)
