from rest_framework.viewsets import ModelViewSet
from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
# from user.service import UserService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.permissions import UserPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# from user.filters import UserFilterSet


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    search_fields = ("first_name", "last_name", "username", "email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("id", "role", "email", "username", "is_active")
    # filterset_class = UserFilterSet


# class TokenAuthView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         user_srv = UserService(request)
#
#         data = user_srv.authenticate_user(request.data)
#
#         return Response(data, status=status.HTTP_200_OK)
#
#
# class RegisterView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         user_srv = UserService(request)
#
#         data = user_srv.register(request.data)
#
#         return Response(data, status=status.HTTP_201_CREATED)
