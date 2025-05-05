from rest_framework import serializers
from warehouse.models import StockMovement
from warehouse.serializers.product import ProductStockSerializer


class StockMovementSerializer(serializers.ModelSerializer):
    product = ProductStockSerializer(read_only=True)

    class Meta:
        model = StockMovement
        fields = "__all__"
        extra_kwargs = {
            "product": {"required": True},
            "quantity": {"required": True},
            "status": {"required": True},
        }


class StockMovementCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            "product",
            "quantity",
        ]
        extra_kwargs = {
            "quantity": {"required": True},
        }
