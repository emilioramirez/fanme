from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView

from registration.backends.default.views import ActivationView

from accounts import views


urlpatterns = patterns('',
    (r'^user/', views.register_user),
    (r'^company/', views.register_company),
    url(r'^login/', views.login_user, name="auth_login"),
    (r'^logout/$', views.logout_user),
    (r'^thanks/', views.thanks),
    (r'^topics/', views.my_topics),
    # Django-registration activations links
    url(r'^activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$',
        ActivationView.as_view(),
        name='registration_activate'),
)
