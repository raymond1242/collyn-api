from rest_framework import routers
from order.views.order import OrderViewSet
from order.views.auth import AuthViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"orders", viewset=OrderViewSet, basename="order")

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

urlpatterns = router.urls
