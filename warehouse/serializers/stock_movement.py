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


class StockeMovementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = [
            "quantity",
        ]
        extra_kwargs = {
            "quantity": {"required": True},
        }

    def update(self, instance, validated_data):
        new_quantity = validated_data.get("quantity")
        old_quantity = instance.quantity
        product = instance.product
        diff = new_quantity - old_quantity

        # Update stock
        if instance.ticket.type == "ENTRY":
            product.stock += diff
        elif instance.ticket.type == "MOVEMENT":
            product.stock -= diff
        else:
            return instance

        if product.stock < 0:
            return instance
        product.save()

        # Save movement
        instance.quantity = new_quantity
        instance.status = StockMovement.EDITED
        instance.save()

        return instance
