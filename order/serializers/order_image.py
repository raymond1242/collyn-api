from rest_framework import serializers
from order.models import OrderImage


class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ["id", "image", "order"]


class OrderImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ["image", "order"]
