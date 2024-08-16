from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class UserCompany(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="company/logos", blank=True, null=True)
    users = models.ManyToManyField(
        UserCompany, through="UserRole", help_text="Users in the company"
    )


class UserRole(models.Model):
    STORE = "STORE"
    ADMIN = "ADMIN"
    ROLE_CHOICES = (
        (STORE, "Store"),
        (ADMIN, "Admin"),
    )
    user = models.ForeignKey(UserCompany, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    product = models.TextField(default="")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="orders"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pending_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    registration_place = models.CharField(max_length=100)
    shipping_place = models.CharField(max_length=100)
    shipping_date = models.DateTimeField()
    has_production = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    @staticmethod
    def generate_code(length=5):
        return uuid4().hex[:length].upper()


class OrderImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="order/images", blank=True, null=True)
