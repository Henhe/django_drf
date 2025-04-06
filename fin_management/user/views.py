from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from user.models import User
from user.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from config.permissions import IsOwnerOfObject
from user.permissions import UserPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, UserPermission, IsOwnerOfObject]
    search_fields = ("first_name", "last_name", "username", "email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("id", "role", "email", "username", "is_active")

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
            return Response({'message':'User logout successfully'},
                            status=status.HTTP_205_RESET_CONTENT)
        except (ObjectDoesNotExist, TokenError) as err:
            return Response({'message':str(err)},status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request method.'},
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)
