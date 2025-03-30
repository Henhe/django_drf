from rest_framework.viewsets import ModelViewSet
from category.models import Category
from category.serializers import CategorySerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [UserPermission]
    search_fields = ("name", "creator__username", "creator__first_name", "creator__last_name", "creator__email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name", "creator__username")