from rest_framework import routers
from order.views.order import OrderViewSet
from order.views.auth import AuthViewSet
from order.views.user_company import UserCompanyViewSet
from order.views.order_image import OrderImageViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"orders", viewset=OrderViewSet, basename="order")

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(prefix=r"company", viewset=UserCompanyViewSet, basename="company")

router.register(
    prefix=r"order/images", viewset=OrderImageViewSet, basename="order_image"
)

urlpatterns = router.urls
