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
    (r'^$', views.redirect),
    (r'^admin/', include(admin.site.urls)),
    (r'^register', accounts_views.register),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
