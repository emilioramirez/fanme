from django.conf.urls.defaults import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/informes/', include('informes.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
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
    (r'^rathings/', include('rathings.urls')),
)


from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )
