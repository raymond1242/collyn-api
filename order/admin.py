from django.contrib import admin
from order.models import Order, OrderImage, Company, UserCompany


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "price",
        "advance_payment",
        "pending_payment",
        "code",
        "shipping_place",
        "shipping_date",
        "completed",
    ]


@admin.register(OrderImage)
class OrderImage(admin.ModelAdmin):
    list_display = ["order", "image"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(UserCompany)
class UserCompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "company", "role"]
