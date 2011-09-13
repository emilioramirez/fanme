from django.conf.urls.defaults import patterns
from fanme.dash import views


urlpatterns = patterns('',
    #(r'^user/', views.register_user),
    (r'^dashboard/', views.dashboard),
    (r'^logbook/', views.logbook),
    (r'^topicos/', views.topicos),
    (r'^results/', views.results),
    (r'^empresa/', views.empresa),
    (r'^follow/(?P<user_id>\d+)$', views.logbook_follow_user),
)
