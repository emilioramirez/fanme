from django.conf.urls.defaults import *
import views
from fanme.accounts import views as accounts_views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^fanme/', include('fanme.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'home', views.home),
    (r'^dashboard', views.dashboard),
    (r'^register', accounts_views.register),
)
