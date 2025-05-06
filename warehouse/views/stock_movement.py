from rest_framework import viewsets, mixins, status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from warehouse.models import StockMovement
from warehouse.serializers.stock_movement import (
    StockMovementSerializer,
    StockMovementCreateSerializer,
    StockeMovementUpdateSerializer,
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class StockMovementViewSet(viewsets.GenericViewSet, mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        queryset = self.get_queryset()
        return queryset.get(id=self.kwargs["id"])

    @swagger_auto_schema(
        request_body=StockeMovementUpdateSerializer,
        responses={status.HTTP_200_OK: StockMovementSerializer},
    )
    def update(self, request, *args, **kwargs):
        stock_movement = self.get_object()
        serializer = StockeMovementUpdateSerializer(stock_movement, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
