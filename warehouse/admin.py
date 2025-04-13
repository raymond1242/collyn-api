from django.contrib import admin
from warehouse.models import UserWarehouse, Ticket, Product, Location


@admin.register(UserWarehouse)
class UserWarehouseAdmin(admin.ModelAdmin):
    list_display = ["user", "company", "role"]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ["type", "created_at", "updated_at", "company", "location"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "min_stock", "stock"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["company", "name"]
