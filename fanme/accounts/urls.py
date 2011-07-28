from django.conf.urls.defaults import *
from fanme.accounts import views


urlpatterns = patterns('',
    (r'^user/', views.register_user),
    (r'^company/', views.register_company),
    (r'^login/', views.login_user),
    (r'^thanks/', views.thanks),    
)
