from rest_framework import serializers

from apps.dataset.models import Order, OrderDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('name', 'description')


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetail
        fields = ('id', 'customer', 'age', 'weight', 'is_vegetarian')

