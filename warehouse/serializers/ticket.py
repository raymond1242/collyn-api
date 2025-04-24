from rest_framework import serializers
from warehouse.models import Ticket
from warehouse.serializers.stock_movement import StockMovementSerializer
from warehouse.serializers.location import LocationSerializer
from warehouse.serializers.user_warehouse import UserWarehouseTicketSerializer


class TicketSerializer(serializers.ModelSerializer):
    movements = StockMovementSerializer(many=True, read_only=True)
    location = LocationSerializer(read_only=True)
    user = UserWarehouseTicketSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"

        extra_kwargs = {
            "type": {"required": True},
        }
