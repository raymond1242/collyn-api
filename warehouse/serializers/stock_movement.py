from django.utils import timezone
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
        ticket = instance.ticket
        diff = new_quantity - old_quantity

        # Update stock
        if ticket.type == "ENTRY":
            product.stock += diff
        elif ticket.type == "MOVEMENT":
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

        ticket.updated_at = timezone.now()
        ticket.save()

        return instance

    def perform_destroy(self):
        instance = self.instance
        product = instance.product
        ticket = instance.ticket
        quantity = instance.quantity

        # Update stock
        if ticket.type == "ENTRY":
            product.stock -= quantity
        elif ticket.type == "MOVEMENT":
            product.stock += quantity
        else:
            return instance

        if product.stock < 0:
            return instance
        product.save()

        # Save movement
        instance.status = StockMovement.DELETED
        instance.save()

        ticket.updated_at = timezone.now()
        ticket.save()


class ProductMovementSummarySerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source="product")
    name = serializers.CharField(source="product__name")
    category = serializers.CharField(source="product__category")
    total_quantity = serializers.IntegerField()
