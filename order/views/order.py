from rest_framework import viewsets
from order.models import Order
from order.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
