from rest_framework import serializers
from warehouse.models import Ticket
from warehouse.serializers.location import LocationSerializer
from warehouse.serializers.stock_movement import (
    StockMovementSerializer,
    StockMovementCreateSerializer,
)
from warehouse.serializers.user_warehouse import UserWarehouseTicketSerializer


class TicketSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    user = UserWarehouseTicketSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            "id",
            "location",
            "user",
            "created_at",
            "type",
        ]

        extra_kwargs = {
            "type": {"required": True},
        }


class TicketDetailSerializer(serializers.ModelSerializer):
    movements = StockMovementSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    user = UserWarehouseTicketSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"

        extra_kwargs = {
            "type": {"required": True},
        }


class TicketCreateSerializer(serializers.ModelSerializer):
    movements = StockMovementCreateSerializer(many=True)

    class Meta:
        model = Ticket
        fields = [
            "type",
            "location",
            "movements",
        ]

    def validate(self, data):
        if data.get("type") == Ticket.MOVEMENT and not data.get("location"):
            raise serializers.ValidationError(
                {"location": "Localidad es obligatoria para movimientos"}
            )
        return data
