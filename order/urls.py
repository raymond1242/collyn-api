from rest_framework import routers
from order.views.order import OrderViewSet
from order.views.auth import AuthViewSet
from order.views.user_company import UserCompanyViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"orders", viewset=OrderViewSet, basename="order")

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(prefix=r"company", viewset=UserCompanyViewSet, basename="company")

urlpatterns = router.urls
