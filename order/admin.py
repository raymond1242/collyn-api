from django.contrib import admin
from order.models import Order, OrderImage, Company


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderImage)
class OrderImage(admin.ModelAdmin):
    list_display = ["order", "image"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]
