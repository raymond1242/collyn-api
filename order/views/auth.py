from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from order.serializers.auth import UserLoginSerializer, TokenSerializer


class AuthViewSet(viewsets.GenericViewSet):
    serializer_class = AuthTokenSerializer

    @swagger_auto_schema(
        methods=["POST"],
        request_body=UserLoginSerializer,
        responses={status.HTTP_200_OK: TokenSerializer},
    )
    @action(methods=["POST"], detail=False, serializer_class=UserLoginSerializer)
    def login(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(TokenSerializer(token).data)
