from rest_framework import serializers
from dj_rest_auth.registration.serializers import (
    RegisterSerializer as DJRegisterSerializer,
)


class RegisterSerializer(DJRegisterSerializer):
    email = None
    password1 = None
    password2 = None
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        return super().validate_password1(value)

    def validate(self, data):
        data["password1"] = data["password"]
        return data
