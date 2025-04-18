from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.permissions import IsCreatorOfObject
from rest_framework import status


# class CategoryViewSet(ModelViewSet):
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ("name", "creator__username", "creator__first_name", "creator__last_name", "creator__email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name", "creator__username")
    # permission_classes = [IsCreatorOfObject, CategoryPermission]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif (self.action == 'update'
              or self.action == 'partial_update'
              or self.action == 'destroy'):
            permission_classes = [IsCreatorOfObject]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
