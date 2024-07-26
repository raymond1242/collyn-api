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
            user = User.objects.get(username=username)
            if user:
                if user.check_password(password):
                    return {"user": user}
            raise serializers.ValidationError("Invalid username or password")
        else:
            raise serializers.ValidationError("Missing username or password")


class TokenSerializer(serializers.Serializer):
    user = UserSerializer(required=True, help_text="User object")

    class Meta:
        model = Token
        fields = ["key"]
