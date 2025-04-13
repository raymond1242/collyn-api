from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from warehouse.serializers.user_warehouse import UserWarehouseSerializer
from drf_yasg.utils import swagger_auto_schema

from warehouse.models import UserWarehouse
from django.contrib.auth.models import User


class UserWarehouseViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserWarehouseSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "user"

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: UserWarehouseSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        user: User = request.user
        user_company = UserWarehouse.objects.get(user=user)
        serializer = self.get_serializer(user_company)
        return Response(serializer.data)
