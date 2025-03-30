from config.service import BaseService
from user.serializers import UserLoginSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.http.response import HttpResponseBadRequest
from rest_framework.authtoken.models import Token


class UserService(BaseService):

    def authenticate_user(self, user_data: dict):
        serializer = UserLoginSerializer(data=user_data)
        # print(serializer.initial_data)
        user = authenticate(
            username=serializer.initial_data.get("username"),
            password=serializer.initial_data.get("password"),
        )

        if not user:
            return {"error": "Invalid password or username"}

        token, _ = Token.objects.get_or_create(user=user)

        return {"token": token.key}

    def register(self, user_data: dict):
        serializer = RegisterSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()

        return UserSerializer(user).data

