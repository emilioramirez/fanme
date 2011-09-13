from django.conf.urls.defaults import patterns
from fanme.items import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    (r'^item/(?P<item_id>\d+)$', views.item),
)
