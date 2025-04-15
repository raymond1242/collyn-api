from rest_framework import mixins, viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from warehouse.models import UserWarehouse, Product
from warehouse.serializers.product import ProductDetailSerializer


class ProductViewset(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
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
            )
        )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
