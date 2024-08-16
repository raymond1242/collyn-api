from uuid import uuid4

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action

from order.models import Order, OrderImage, UserCompany
from order.serializers.order import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderUpdateCompletedSerializer,
    OrderUpdateStoreSerializer,
    OrderUpdateAdminSerializer,
)

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


def generate_code(length=5):
    return uuid4().hex[:length].upper()


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    queryset = Order.objects.all()

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_user_company(self):
        return self.request.user.user_company

    def get_queryset(self):
        company = self.get_user_company().company
        return (
            super(OrderViewSet, self)
            .get_queryset()
            .filter(
                company=company,
            )
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "shipping_start_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="shipping_start_date",
            ),
            openapi.Parameter(
                "shipping_end_date",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="shipping_date",
            ),
            openapi.Parameter(
                "shipping_place",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="shipping_place",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        shipping_start_date = request.query_params.get("shipping_start_date")
        shipping_end_date = request.query_params.get("shipping_end_date")
        shipping_place = request.query_params.get("shipping_place")

        queryset = self.queryset

        if shipping_start_date and shipping_end_date:
            queryset = queryset.filter(
                shipping_date__range=[shipping_start_date, shipping_end_date]
            )

        if shipping_place:
            queryset = queryset.filter(shipping_place=shipping_place)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderCreateSerializer,
        responses={status.HTTP_201_CREATED: OrderSerializer},
    )
    def create(self, request, *args, **kwargs):
        user = self.get_user_company()
        company = user.company
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        images = serializer.validated_data.pop("images")
        order = serializer.save(company=company)

        for image in images:
            OrderImage.objects.create(order=order, image=image)

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=OrderUpdateCompletedSerializer,
        responses={status.HTTP_200_OK: OrderSerializer},
    )
    @action(
        methods=["PUT"], detail=True, serializer_class=OrderUpdateCompletedSerializer
    )
    def update_completed(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order.completed = serializer.validated_data["completed"]
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderUpdateAdminSerializer,
        responses={status.HTTP_200_OK: OrderSerializer},
    )
    def update(self, request, *args, **kwargs):
        order = self.get_object()
        user = self.get_user_company()

        if user.role == UserCompany.STORE:
            serializer = OrderUpdateStoreSerializer(order, data=request.data)
        elif user.role == UserCompany.ADMIN:
            serializer = OrderUpdateAdminSerializer(order, data=request.data)
        else:
            raise Exception("Invalid role")

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
