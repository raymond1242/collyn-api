from django.contrib import admin
from order.models import Order, OrderImage, Company, Location


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderImage)
class OrderImage(admin.ModelAdmin):
    list_display = ("order", "image")

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
