from datetime import timedelta
from rest_framework import viewsets, mixins, status

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from django.utils import timezone
from django.db.models import Sum
from warehouse.models import StockMovement, Ticket, UserWarehouse
from warehouse.serializers.stock_movement import (
    StockMovementSerializer,
    StockeMovementUpdateSerializer,
    ProductMovementSummarySerializer,
)

from drf_yasg import openapi
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
        stock_movement.updated_at = timezone.now()
        stock_movement.save()
        return Response(
            StockMovementSerializer(stock_movement).data, status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        stock_movement = self.get_object()
        serializer = StockeMovementUpdateSerializer(stock_movement)
        serializer.perform_destroy()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "type",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Type of ticket",
                required=True,
                default=Ticket.ENTRY,
            ),
            openapi.Parameter(
                "start_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="start_date",
                required=True,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="end_date",
                required=True,
            ),
            openapi.Parameter(
                "location",
                openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="location id",
                required=False,
            ),
        ],
        responses={status.HTTP_200_OK: ProductMovementSummarySerializer(many=True)},
    )
    @action(methods=["GET"], detail=False)
    def products(self, request):
        user = self.request.user
        company = UserWarehouse.objects.get(user=user).company

        ticket_type = request.query_params.get("type", Ticket.ENTRY)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        location = request.query_params.get("location")

        location_filter = {}
        if location and ticket_type == Ticket.MOVEMENT:
            location_filter["ticket__location"] = location

        queryset = (
            StockMovement.objects.filter(
                ticket__company=company,
                ticket__type=ticket_type,
                status__in=[StockMovement.EDITED, StockMovement.NOT_EDITED],
                ticket__created_at__range=[start_date, end_date],
                **location_filter,
            )
            .values("product", "product__name", "product__category")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("product__category")
        )

        serializer = ProductMovementSummarySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductMovementSummarySerializer(many=True)},
    )
    @action(methods=["GET"], detail=False)
    def top_products(self, request):
        user = self.request.user
        company = UserWarehouse.objects.get(user=user).company

        now = timezone.now()
        start_date = now - timedelta(days=30)
        end_date = now + timedelta(days=1)

        queryset = (
            StockMovement.objects.filter(
                ticket__company=company,
                ticket__type=Ticket.MOVEMENT,
                ticket__created_at__range=[start_date, end_date],
                status__in=[StockMovement.EDITED, StockMovement.NOT_EDITED],
            )
            .values("product", "product__name", "product__category")
            .annotate(total_quantity=Sum("quantity"))
            .order_by("-total_quantity")[:10]
        )

        serializer = ProductMovementSummarySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
