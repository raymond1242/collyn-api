from rest_framework import viewsets, mixins, status
from order.models import Order, OrderImage
from order.serializers.order import OrderSerializer, OrderCreateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class OrderViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    # def get_queryset(self):
    #     company = self.request.user.company
    #     return Order.objects.filter(company=company)

    @swagger_auto_schema(
        request_body=OrderCreateSerializer,
        responses={status.HTTP_201_CREATED: OrderSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images = serializer.validated_data.pop("images")
        order = serializer.save(company=self.request.user.company)

        for image in images:
            OrderImage.objects.create(order=order, image=image)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
