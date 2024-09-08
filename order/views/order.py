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


class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    queryset = Order.objects.all()

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_user_company(self):
        user_company = UserCompany.objects.get(user=self.request.user)
        return user_company

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
            openapi.Parameter(
                "has_production",
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="has_production",
            ),
            openapi.Parameter(
                "has_topper",
                openapi.IN_QUERY,
                type=openapi.TYPE_BOOLEAN,
                description="has_topper",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        shipping_start_date = request.query_params.get("shipping_start_date")
        shipping_end_date = request.query_params.get("shipping_end_date")
        shipping_place = request.query_params.get("shipping_place")
        has_production = request.query_params.get("has_production")
        has_topper = request.query_params.get("has_topper")

        queryset = self.get_queryset().filter(completed=False)

        if shipping_start_date and shipping_end_date:
            queryset = queryset.filter(
                shipping_date__range=[shipping_start_date, shipping_end_date]
            )

        if shipping_place:
            queryset = queryset.filter(shipping_place=shipping_place)

        if has_production == "true":
            queryset = queryset.filter(has_production=True)

        if has_topper == "true":
            queryset = queryset.filter(has_topper=True)

        queryset = queryset.order_by("shipping_date")
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        ],
        responses={status.HTTP_200_OK: OrderSerializer(many=True)},
    )
    @action(methods=["GET"], detail=False, serializer_class=OrderSerializer)
    def completed(self, request):
        shipping_start_date = request.query_params.get("shipping_start_date")
        shipping_end_date = request.query_params.get("shipping_end_date")
        shipping_place = request.query_params.get("shipping_place")

        orders = self.get_queryset().filter(completed=True)

        if shipping_start_date and shipping_end_date:
            orders = orders.filter(
                shipping_date__range=[shipping_start_date, shipping_end_date]
            )

        if shipping_place:
            orders = orders.filter(shipping_place=shipping_place)

        serializer = self.get_serializer(orders, many=True)
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

        images = serializer.validated_data.pop("images", [])

        code = Order.generate_unique_code()
        while Order.objects.filter(code=code).exists():
            code = Order.generate_unique_code()

        order = serializer.save(company=company, code=code)

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
        request_body=OrderUpdateStoreSerializer,
        responses={status.HTTP_200_OK: OrderSerializer},
    )
    @action(methods=["PUT"], detail=True, serializer_class=OrderUpdateStoreSerializer)
    def update_store(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=OrderUpdateAdminSerializer,
        responses={status.HTTP_200_OK: OrderSerializer},
    )
    @action(methods=["PUT"], detail=True, serializer_class=OrderUpdateAdminSerializer)
    def update_admin(self, request, pk=None):
        order = self.get_object()
        serializer = self.get_serializer(order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
