from rest_framework import routers
from warehouse.views.auth import AuthViewSet
from warehouse.views.user_warehouse import UserWarehouseViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(
    prefix=r"user_warehouse", viewset=UserWarehouseViewSet, basename="user_warehouse"
)

urlpatterns = router.urls
