from rest_framework import serializers
from django.contrib.auth.models import User
from order.serializers.company import CompanySerializer
from warehouse.models import UserWarehouse


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class UserWarehouseLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                raise serializers.ValidationError("Usuario o contraseña incorrectos")

            if user.check_password(password):
                return {"user": user}
            raise serializers.ValidationError("Usuario o contraseña incorrectos")
        else:
            raise serializers.ValidationError(
                "Falta el nombre de usuario o la contraseña"
            )


class WarehouseTokenSerializer(serializers.Serializer):
    key = serializers.CharField(required=True)
    user = UserDetailSerializer(required=True, help_text="User object")
