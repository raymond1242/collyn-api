from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from order.models import Order, OrderImage
from order.serializers.order import OrderSerializer, OrderCreateSerializer, OrderUpdateDeliveredSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class OrderViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(responses={status.HTTP_200_OK: OrderSerializer(many=True)})
    def list(self, request, *args, **kwargs):
        company = self.request.user.company
        return super().list(request, *args, company=company, **kwargs)

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

    @swagger_auto_schema(
        request_body=OrderUpdateDeliveredSerializer,
        responses={status.HTTP_200_OK: OrderSerializer},
    )
    @action(methods=["PUT"], detail=True, serializer_class=OrderUpdateDeliveredSerializer)
    def update_delivered(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order.delivered = serializer.validated_data["delivered"]
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
