from django.conf.urls.defaults import patterns, include
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.redirect),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('fanme.accounts.urls')),
    (r'^dash/', include('fanme.dash.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
