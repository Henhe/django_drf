from django.contrib.auth import authenticate
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
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    search_fields = ("first_name", "last_name", "username", "email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("id", "role", "email", "username", "is_active")
    # filterset_class = UserFilterSet


class RegistrationAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user) # Создание Refesh и Access
            refresh.payload.update({    # Полезная информация в самом токене
                'user_id': user.id,
                'username': user.username
            })

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), # Отправка на клиент

            }, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username', None)
        password = data.get('password', None)
        if username is None or password is None:
            return Response({'error': 'Need login and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({'error': 'No user'},
                            status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'username': user.username
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token') # С клиента нужно отправить refresh token
        if not refresh_token:
            return Response({'error': 'Need Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist() # Добавить его в чёрный список

        except Exception as e:
            return Response({'error': 'No Refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': 'Logout success'}, status=status.HTTP_200_OK)
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
