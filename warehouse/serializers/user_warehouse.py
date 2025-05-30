from rest_framework import serializers
from warehouse.models import UserWarehouse
from order.serializers.company import CompanySerializer
from warehouse.serializers.auth import UserDetailSerializer


class UserWarehouseSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=True, help_text="User object")
    company = CompanySerializer()

    class Meta:
        model = UserWarehouse
        fields = ["user", "role", "company"]


class UserWarehouseTicketSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(required=True, help_text="User object")

    class Meta:
        model = UserWarehouse
        fields = ["user", "role"]
