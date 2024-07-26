from rest_framework import serializers
from order.models import Order, Company, Location, OrderImage


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True, source="orderimage_set")

    class Meta:
        model = Order
        fields = "__all__"


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
