from rest_framework import serializers
from warehouse.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "min_stock",
            "stock",
            "image",
        ]

        extra_kwargs = {
            "min_stock": {"required": True},
            "stock": {"required": True},
            "category": {"required": True},
        }
