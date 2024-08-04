from rest_framework import serializers
from order.models import Order, Company, Location, OrderImage


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ["image"]


class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    shipping_date = serializers.DateTimeField(input_formats=["%Y-%m-%dT%H:%M"])

    class Meta:
        model = Order
        fields = [
            "name",
            "description",
            "price",
            "advance_payment",
            "discount",
            "pending_payment",
            "registration_place",
            "shipping_place",
            "shipping_date",
            "has_production",
            "delivered",
            "images",
        ]
