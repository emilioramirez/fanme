from django.conf.urls.defaults import patterns, include
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.redirect),
    (r'^home/$', views.home),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('fanme.accounts.urls')),
    (r'^dash/', include('fanme.dash.urls')),
    (r'^items/', include('fanme.items.urls')),
    (r'^social/', include('fanme.social.urls')),
    (r'^bussiness/', include('fanme.social.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^mymedia/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
