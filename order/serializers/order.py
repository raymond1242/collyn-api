from rest_framework import serializers
from order.models import Order
from order.serializers.order_image import OrderImageSerializer


class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderUpdateCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["completed"]


class OrderUpdateStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["advance_payment", "pending_payment", "shipping_date"]
        extra_kwargs = {field: {"required": False} for field in fields}


class OrderUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "name",
            "product",
            "description",
            "price",
            "advance_payment",
            "pending_payment",
            "registration_place",
            "shipping_place",
            "shipping_date",
            "has_production",
            "has_delivery",
            "completed",
        ]
        extra_kwargs = {field: {"required": False} for field in fields}


class OrderCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    shipping_date = serializers.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])

    class Meta:
        model = Order
        fields = [
            "name",
            "product",
            "description",
            "price",
            "advance_payment",
            "discount",
            "pending_payment",
            "registration_place",
            "shipping_place",
            "shipping_date",
            "has_production",
            "has_delivery",
            "has_topper",
            "images",
        ]
