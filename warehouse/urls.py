from rest_framework import routers
from warehouse.views.auth import AuthViewSet
from warehouse.views.user_warehouse import UserWarehouseViewSet
from warehouse.views.product import ProductViewset
from warehouse.views.ticket import TicketViewSet
from warehouse.views.location import LocationViewSet
from warehouse.views.stock_movement import StockMovementViewSet

router = routers.DefaultRouter(trailing_slash=False)

router.register(prefix=r"auth", viewset=AuthViewSet, basename="auth")

router.register(
    prefix=r"user_warehouse", viewset=UserWarehouseViewSet, basename="user_warehouse"
)

router.register(prefix=r"product", viewset=ProductViewset, basename="product")

router.register(prefix=r"ticket", viewset=TicketViewSet, basename="ticket")

router.register(prefix=r"location", viewset=LocationViewSet, basename="location")

router.register(
    prefix=r"stock_movement", viewset=StockMovementViewSet, basename="stock_movement"
)

urlpatterns = router.urls
