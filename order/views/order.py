from rest_framework import viewsets
from order.models import Order
from order.serializers.order import OrderSerializer

# from order.permissions import IsOwnerOrReadOnly


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = [IsOwnerOrReadOnly]
