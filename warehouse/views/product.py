from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.decorators import action
from django.db.models import F

from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from warehouse.models import UserWarehouse, Product
from warehouse.serializers.product import (
    ProductDetailSerializer,
    ProductStockSerializer,
    ProductCreateSerializer,
    ProductDeleteSerializer,
    ProductUpdateSerializer,
)


class ProductViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    authentication_classes = [TokenAuthentication]

    def get_user_company(self):
        user_company = UserWarehouse.objects.get(user=self.request.user)
        return user_company

    def get_queryset(self):
        company = self.get_user_company().company
        return (
            super(ProductViewset, self)
            .get_queryset()
            .filter(
                company=company,
                deleted=False,
            )
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ProductCreateSerializer,
        responses={status.HTTP_201_CREATED: ProductDetailSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save(company=self.get_user_company().company)
        headers = self.get_success_headers(serializer.data)
        return Response(
            ProductDetailSerializer(product).data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @swagger_auto_schema(
        request_body=ProductUpdateSerializer,
        responses={status.HTTP_200_OK: ProductDetailSerializer},
    )
    def update(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = ProductUpdateSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            ProductDetailSerializer(product).data,
            status=status.HTTP_200_OK,
            headers=headers,
        )

    def destroy(self, request, *args, **kwargs):
        stock_movement = self.get_object()
        serializer = ProductDeleteSerializer(stock_movement)
        serializer.perform_destroy()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ProductStockSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, serializer_class=ProductStockSerializer)
    def stock(self, request, pk=None):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, serializer_class=ProductStockSerializer)
    def low_stock(self, request, pk=None):
        queryset = self.get_queryset()
        low_stock = queryset.filter(stock__lte=F("min_stock"))[:8]
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
