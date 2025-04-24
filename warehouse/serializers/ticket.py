from rest_framework import serializers
from warehouse.models import Ticket


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ["id", "type", "created_at", "updated_at", "location", "user"]

        extra_kwargs = {
            "type": {"required": True},
        }
