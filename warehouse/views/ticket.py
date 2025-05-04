from rest_framework import viewsets, mixins, status

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from warehouse.models import Ticket, UserWarehouse
from warehouse.serializers.ticket import TicketSerializer, TicketDetailSerializer

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class TicketViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
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
        ]
    )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        type = request.query_params.get("type", Ticket.ENTRY)
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
