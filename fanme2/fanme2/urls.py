from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'fanme2.views.home', name='home'),
    # url(r'^fanme2/', include('fanme2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('accounts.urls')),
    # django-registration urls
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^dashboard/', 'fanme2.views.dashboard', name='dashboard'),
    url(r'^logbook/', 'fanme2.views.logbook', name='logbook'),
    url(r'^core/', include('core.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
