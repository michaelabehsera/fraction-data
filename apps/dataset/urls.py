from django.conf.urls import url

from .views import OrderCreateView


app_name = 'dataset'

urlpatterns = [

    url(r'^create_order/$', OrderCreateView.as_view(), name='creat_order'),
]
