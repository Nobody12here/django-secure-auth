from rest_framework import serializers
from .models import User


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                "Password and confirm password are different!"
            )
        email = data["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "User is registered already\nPlease login"
            )
        return data


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
