from django.conf.urls import url, include
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from rest_framework_swagger.views import get_swagger_view

from api.v1.urls import api_v1_router


swagger_doc = get_swagger_view(title='Fraction Data API')

urlpatterns = [

    url(r'', include('apps.common.urls')),
    url(r'^account/', include('apps.accounts.urls')),
    url(r'^dataset/', include('apps.dataset.urls')),

    url(r'^api/v1/', include(api_v1_router.urls)),
    url(r'^api/docs/', swagger_doc),

    url(r'^admin/', admin.site.urls),
]

admin.site.site_header = _("Fraction Data Administration")
admin.site.site_title = _("Fraction Data")
