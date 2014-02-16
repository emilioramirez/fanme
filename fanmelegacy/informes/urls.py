from django.conf.urls.defaults import patterns
from informes import views


urlpatterns = patterns('',
    (r'^mypage/', views.my_admin_view),
    (r'^progreso/', views.progreso),
    (r'^progreso_anios/(?P<cant_anios>\d+)/$', views.progreso_anios),
    (r'^fans_por_topicos/', views.fans_por_topicos),
    (r'^fans_por_subtopico/', views.fans_por_sub_topicos),
    (r'^item_fans/', views.item_fans),
    (r'^item_fanes/(?P<cant_items>\d+)/$', views.cant_items_fans),
    (r'^item_fanes/(?P<item_id>\d+)/$', views.informe_item_filtrado),
    (r'^progreso_filtrado/$', views.progreso_filtrado),
)
