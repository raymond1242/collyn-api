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


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "category", "stock"]
        extra_kwargs = {
            "category": {"required": True},
            "stock": {"required": True},
            "name": {"required": True},
        }


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
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


class ProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["deleted"]
        extra_kwargs = {
            "deleted": {"required": True},
        }

    def perform_destroy(self):
        instance = self.instance
        instance.deleted = True
        instance.save()


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "min_stock",
        ]
