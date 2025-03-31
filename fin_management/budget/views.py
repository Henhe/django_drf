from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from budget.models import Budget
from budget.serializers import BudgetSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.permissions import IsCreatorOfObject


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    search_fields = ("name", "creator__username", "creator__first_name", "creator__last_name", "creator__email", "sum")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name", "creator__username", "sum")
    permission_classes = [IsCreatorOfObject, ]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
