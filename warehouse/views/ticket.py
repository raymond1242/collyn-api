from rest_framework import viewsets, mixins, status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from warehouse.models import Ticket, UserWarehouse, StockMovement
from warehouse.serializers.ticket import (
    TicketSerializer,
    TicketDetailSerializer,
    TicketCreateSerializer,
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class TicketViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = [TokenAuthentication]

    def get_user_company(self):
        user_company = UserWarehouse.objects.get(user=self.request.user)
        return user_company

    def get_queryset(self):
        company = self.get_user_company().company
        return (
            super(TicketViewSet, self)
            .get_queryset()
            .filter(
                company=company,
            )
        )

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
                required=False,
            ),
            openapi.Parameter(
                "end_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="end_date",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        type = request.query_params.get("type", Ticket.ENTRY)
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if start_date and end_date:
            queryset = queryset.filter(
                created_at__range=[start_date, end_date]
            )

        queryset = queryset.filter(type=type)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TicketDetailSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        # company = self.get_user_company().company
        ticket = self.get_object()
        serializer = TicketDetailSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TicketCreateSerializer,
        responses={status.HTTP_201_CREATED: TicketDetailSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = self.get_user_company()
        company = user.company

        serializer = TicketCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        movements = serializer.validated_data.pop("movements", [])
        if not movements:
            return Response(
                {"movements": ["El ticket debe contener al menos un movimiento."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        ticket = serializer.save(company=company, user=user)

        for movement in movements:
            movement = StockMovement.objects.create(
                ticket=ticket, status=StockMovement.NOT_EDITED, **movement
            )
            if ticket.type == Ticket.ENTRY:
                movement.product.stock += movement.quantity
                movement.product.save()
            elif ticket.type == Ticket.MOVEMENT:
                if movement.product.stock - movement.quantity < 0:
                    movement.status = StockMovement.DELETED
                    movement.save()
                else:
                    movement.product.stock -= movement.quantity
                    movement.product.save()

        serializer = TicketDetailSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
