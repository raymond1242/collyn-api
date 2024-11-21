import string
import random
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="company/logos", blank=True, null=True)


class UserCompany(models.Model):
    STORE = "STORE"
    ADMIN = "ADMIN"
    ROLE_CHOICES = (
        (STORE, "Store"),
        (ADMIN, "Admin"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="users", null=True
    )
    address = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default=STORE)


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
    has_topper = models.BooleanField(default=False)
    has_delivery = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    code = models.CharField(max_length=255, blank=True, unique=True)
    phone_number = models.CharField(max_length=12, blank=True, default="")

    @staticmethod
    def generate_unique_code(length=5):
        characters = string.ascii_uppercase + string.digits
        return "".join(random.choices(characters, k=length))


class OrderImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="order/images", blank=True, null=True)
