from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

import oauth2_provider.views as oauth2_views


# OAuth2 provider endpoints
oauth2_endpoint_views = [
    url(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    url(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    url(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

urlpatterns = [

    url(r'', include('apps.common.urls')),
    url(r'^account/', include('apps.accounts.urls')),

    url(r'^admin/', admin.site.urls),

    url(r'^o/', include(oauth2_endpoint_views)),

]

admin.site.site_header = _("Fraction Data Administration")
admin.site.site_title = _("Fraction Data")
