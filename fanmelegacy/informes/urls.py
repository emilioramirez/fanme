from django.conf.urls.defaults import patterns
from informes import views


urlpatterns = patterns('',
    (r'^mypage/', views.my_admin_view),
    (r'^progreso/', views.progreso),
    (r'^fans_por_topicos/', views.fans_por_topicos),
)
