from rest_framework import routers

from .views import OrderViewSet, OrderDetailViewSet

api_v1_router = routers.SimpleRouter()
api_v1_router.register(r'^orders', OrderViewSet)
api_v1_router.register(r'^order/(?P<order_id>[0-9]+)/data', OrderDetailViewSet, base_name='order_data')
