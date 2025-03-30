from rest_framework.serializers import ModelSerializer #, IntegerField, CharField, EmailField
from user.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user