from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from warehouse.serializers.auth import (
    UserWarehouseLoginSerializer,
    WarehouseTokenSerializer,
)


class AuthViewSet(viewsets.GenericViewSet):

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserWarehouseLoginSerializer,
        responses={status.HTTP_200_OK: WarehouseTokenSerializer},
    )
    @action(
        methods=["POST"], detail=False, serializer_class=UserWarehouseLoginSerializer
    )
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(WarehouseTokenSerializer(token).data)
