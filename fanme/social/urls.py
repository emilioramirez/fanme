from django.conf.urls.defaults import patterns
from fanme.social import views


urlpatterns = patterns('',
    (r'^messages/$', views.messages),
    (r'^new_message/$', views.new_message),
    (r'^messages_user/(?P<user_id>\d+)$', views.messages_user),
)
