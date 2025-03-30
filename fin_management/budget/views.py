from rest_framework.viewsets import ModelViewSet
from budget.models import Budget
from budget.serializers import BudgetSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    # permission_classes = [UserPermission]
    search_fields = ("name", "creator__username", "creator__first_name", "creator__last_name", "creator__email", "sum")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name", "creator__username", "sum")