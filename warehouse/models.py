from django.db import models
from order.models import Company
from django.contrib.auth.models import User


class Location(models.Model):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="locations"
    )
    name = models.CharField(max_length=255)


class UserWarehouse(models.Model):
    ADMIN = "ADMIN"
    STOCK_MANAGER = "STOCK_MANAGER"
    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (STOCK_MANAGER, "Stock Manager"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=STOCK_MANAGER)


class Product(models.Model):
    CLEANING = "CLEANING"
    DISPOSABLE = "DISPOSABLE"
    SUPPLIES = "SUPPLIES"
    SAUSAGES = "SAUSAGES"
    CATEGORY_CHOICES = (
        (CLEANING, "Cleaning"),
        (DISPOSABLE, "Disposable"),
        (SUPPLIES, "Supplies"),
        (SAUSAGES, "Sausages"),
    )
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(
        max_length=255, choices=CATEGORY_CHOICES, default=CLEANING
    )
    min_stock = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to="product/images", blank=True, null=True)


class Ticket(models.Model):
    ENTRY = "ENTRY"
    MOVEMENT = "MOVEMENT"
    TYPE_CHOICES = (
        (ENTRY, "Entry"),
        (MOVEMENT, "Movement"),
    )
    type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=ENTRY)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True
    )
    user = models.ForeignKey(UserWarehouse, on_delete=models.CASCADE)


class StockMovement(models.Model):
    NOT_EDITED = "NOT_EDITED"
    EDITED = "EDITED"
    DELETED = "DELETED"
    STATUS_CHOICES = (
        (NOT_EDITED, "Not Edited"),
        (EDITED, "Edited"),
        (DELETED, "Deleted"),
    )
    ticket = models.ForeignKey(
        Ticket, on_delete=models.CASCADE, related_name="movements"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=NOT_EDITED)
    updated_at = models.DateTimeField(auto_now=True)
