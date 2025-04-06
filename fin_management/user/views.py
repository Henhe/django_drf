from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError

from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from config.permissions import IsOwnerOfObject
from rest_framework.views import APIView
# from user.service import UserService

from rest_framework import status

from user.permissions import UserPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
# from user.filters import UserFilterSet
from rest_framework_simplejwt.tokens import RefreshToken


from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import LoginSerializer, RegistrationSerializer
# from user.renderers import UserJSONRenderer
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission, IsOwnerOfObject]
    search_fields = ("first_name", "last_name", "username", "email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("id", "role", "email", "username", "is_active")
    # filterset_class = UserFilterSet


# class LogoutView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         try:
#             refresh_token = request.data["refresh_token"]
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#
#             return Response(status=status.HTTP_205_RESET_CONTENT)
#         except Exception as e:
#             print(f'{e=}')
#             return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def logout(request):
    if request.method == 'POST':
        # Access the refresh token from request headers or cookies
        try:
            print(f'{request.META.get('HTTP_AUTHORIZATION', '').split()[1]=}')
            # refresh_token = request.data["refresh"]
            refresh_token = request.META.get('HTTP_AUTHORIZATION', '').split()[1]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'User logout successfully'},status=status.HTTP_205_RESET_CONTENT)
        except (ObjectDoesNotExist, TokenError) as err:
            return Response({'message':str(err)},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request method.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
# class RegistrationAPIView(APIView):
#     """
#     Разрешить всем пользователям (аутентифицированным и нет) доступ к данному эндпоинту.
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = RegistrationSerializer
#     renderer_classes = (UserJSONRenderer,)
#
#     def post(self, request):
#         user = request.data.get('user', {})
#
#         # Паттерн создания сериализатора, валидации и сохранения - довольно
#         # стандартный, и его можно часто увидеть в реальных проектах.
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class LoginAPIView(APIView):
#     permission_classes = (AllowAny,)
#     renderer_classes = (UserJSONRenderer,)
#     serializer_class = LoginSerializer
#
#     def post(self, request):
#         user = request.data.get('user', {})
#         print(f'{request.data=}')
#         print(f'{user=}')
#         # Обратите внимание, что мы не вызываем метод save() сериализатора, как
#         # делали это для регистрации. Дело в том, что в данном случае нам
#         # нечего сохранять. Вместо этого, метод validate() делает все нужное.
#         serializer = self.serializer_class(data=user)
#         # serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class RegistrationAPIView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             refresh = RefreshToken.for_user(user) # Создание Refesh и Access
#             refresh.payload.update({    # Полезная информация в самом токене
#                 'user_id': user.id,
#                 'username': user.username
#             })
#
#             return Response({
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token), # Отправка на клиент
#
#             }, status=status.HTTP_201_CREATED)
#
#
# class LoginAPIView(APIView):
#     def post(self, request):
#         data = request.data
#         username = data.get('username', None)
#         password = data.get('password', None)
#         if username is None or password is None:
#             return Response({'error': 'Need login and password'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(username=username, password=password)
#         if user is None:
#             return Response({'error': 'No user'},
#                             status=status.HTTP_401_UNAUTHORIZED)
#         refresh = RefreshToken.for_user(user)
#         refresh.payload.update({
#             'user_id': user.id,
#             'username': user.username
#         })
#
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }, status=status.HTTP_200_OK)
#
#
# class LogoutAPIView(APIView):
#     def post(self, request):
#         refresh_token = request.data.get('refresh_token') # С клиента нужно отправить refresh token
#         if not refresh_token:
#             return Response({'error': 'Need Refresh token'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist() # Добавить его в чёрный список
#
#         except Exception as e:
#             return Response({'error': 'No Refresh token'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         return Response({'success': 'Logout success'}, status=status.HTTP_200_OK)
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
