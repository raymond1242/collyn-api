from django.contrib import admin
from order.models import Order, Company, Location


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "user")


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass
