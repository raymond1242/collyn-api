from drf_yasg.utils import swagger_auto_schema

from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.models import OrderImage
from order.serializers.order_image import (
    OrderImageSerializer,
    OrderImageCreateSerializer,
)


class OrderImageViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = OrderImage.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderImageSerializer

    @swagger_auto_schema(
        request_body=OrderImageCreateSerializer,
        responses={status.HTTP_201_CREATED: OrderImageSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = OrderImageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_image = serializer.save()

        return Response(
            OrderImageSerializer(order_image).data,
            status=status.HTTP_201_CREATED,
        )
