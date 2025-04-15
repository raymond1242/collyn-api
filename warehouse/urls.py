from rest_framework import routers
from warehouse.views.auth import AuthViewSet
from warehouse.views.user_warehouse import UserWarehouseViewSet
from warehouse.views.product import ProductViewset

router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(
    prefix=r"user_warehouse", viewset=UserWarehouseViewSet, basename="user_warehouse"
)

router.register(prefix=r"product", viewset=ProductViewset, basename="product")

urlpatterns = router.urls
