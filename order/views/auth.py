from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema

from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from order.serializers.auth import UserLoginSerializer, TokenSerializer
from order.serializers.company import UserCompanySerializer

from order.models import UserCompany
from django.contrib.auth.models import User


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


class UserCompanyViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = UserCompanySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    lookup_field = "user"

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: UserCompanySerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        user: User = request.user
        company = UserCompany.objects.get(user=user).company
        serializer = self.get_serializer(company)
        return Response(serializer.data)
