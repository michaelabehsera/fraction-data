from django.conf.urls import url

from .views import OrderCreateView, OrderDetailView


app_name = 'dataset'

urlpatterns = [

    url(r'^create_order/$', OrderCreateView.as_view(), name='creat_order'),
    url(r'^order_detail/(?P<order_id>[0-9]+)/$', OrderDetailView.as_view(), name='order_detail'),
]
