
from rest_framework import viewsets, status

from .serializers import OrderSerializer, OrderDetailSerializer
from apps.dataset.models import Order, OrderDetail


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Order
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderDetailViewSet(viewsets.ModelViewSet):
    """
    API endpoint for OrderDetail

    * {order_id}: Order ID
    * {id}: OrderDetail ID
    """

    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        try:
            order_obj = Order.objects.get(id=self.kwargs['order_id'])
            return OrderDetail.objects.filter(order=order_obj)
        except Order.DoesNotExist:
            return []

    def perform_create(self, serializer):
        try:
            order_obj = Order.objects.get(id=self.kwargs['order_id'])
            serializer.save(order=order_obj)

        except Order.DoesNotExist:
            pass

    def perform_update(self, serializer):
        try:
            order_obj = Order.objects.get(id=self.kwargs['order_id'])
            serializer.save(order=order_obj)

        except Order.DoesNotExist:
            pass
