from django.conf.urls.defaults import patterns, include
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', views.redirect),
    (r'^home/$', views.home),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('accounts.urls')),
    (r'^dash/', include('dash.urls')),
    (r'^items/', include('items.urls')),
    (r'^social/', include('social.urls')),
    (r'^bussiness/', include('bussiness.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^avatar/', include('avatar.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
