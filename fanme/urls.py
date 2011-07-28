from django.conf.urls.defaults import *
import views
#~ from fanme.accounts import views as accounts_views
import fanme

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
    (r'^dashboard/', views.dashboard),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('fanme.accounts.urls')),
    #~ (r'^accounts/login/$', 'django.contrib.auth.views.login'),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
