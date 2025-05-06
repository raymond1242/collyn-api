from rest_framework import viewsets, mixins, status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from warehouse.models import StockMovement
from warehouse.serializers.stock_movement import (
    StockMovementSerializer,
    StockeMovementUpdateSerializer,
)

from drf_yasg.utils import swagger_auto_schema


class StockMovementViewSet(
    viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    permission_classes = [IsAuthenticated]
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    authentication_classes = [TokenAuthentication]

    @swagger_auto_schema(
        request_body=StockeMovementUpdateSerializer,
        responses={status.HTTP_200_OK: StockMovementSerializer},
    )
    def update(self, request, *args, **kwargs):
        stock_movement = self.get_object()
        serializer = StockeMovementUpdateSerializer(stock_movement, data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_movement = serializer.save()
        return Response(
            StockMovementSerializer(stock_movement).data, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        stock_movement = self.get_object()
        serializer = StockeMovementUpdateSerializer(stock_movement)
        serializer.perform_destroy()
        return Response(status=status.HTTP_204_NO_CONTENT)
