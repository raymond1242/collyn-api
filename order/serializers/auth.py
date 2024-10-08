from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class UserLoginSerializer(serializers.Serializer):
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


class TokenSerializer(serializers.Serializer):
    user = UserSerializer(required=True, help_text="User object")
    key = serializers.CharField(required=True, help_text="Token key")

    class Meta:
        model = Token
        fields = ["user", "key"]
