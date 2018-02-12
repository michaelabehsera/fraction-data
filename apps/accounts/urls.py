from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import SignupView
from .forms import LoginForm


app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$', SignupView.as_view(), name='signup'),

    url(r'^login/$',
        auth_views.login,
        {'template_name': 'accounts/signin.html', 'authentication_form': LoginForm},
        name='auth_login'),

    url(r'^logout/$', auth_views.logout_then_login, name='auth_logout'),
]
