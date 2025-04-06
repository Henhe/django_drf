from django.template.context_processors import request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from budget.models import Budget, Funds
from user.models import User
from budget.serializers import BudgetSerializer, FundsSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.permissions import IsCreatorOfObject
from budget.permissions import IsCreatorOrOwnerOfBudgetExecution, BudgetPermission, Funds, FundsPermission


class BudgetViewSet(ModelViewSet):
    #print(f'{request.user=}')
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    search_fields = ("name", "creator__username", "creator__first_name", "creator__last_name", "creator__email", "sum")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("name", "creator__username", "sum")
    permission_classes = [IsCreatorOfObject, BudgetPermission]

    def create(self, request, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        # print(f'{request.data=}')
        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

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


class FundsViewSet(ModelViewSet):
    queryset = Funds.objects.all()
    serializer_class = FundsSerializer
    search_fields = ("budget_name", "creator__username", "creator__first_name", "creator__last_name", "creator__email", "sum")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("budget__name", "creator__username", "sum")

    def create(self, request, *args, **kwargs):
        print(f"{request.data=}")
        data = request.data
        data['creator'] = User.objects.filter(pk=data.get('creator')).first().pk
        data['creator_id'] = User.objects.filter(pk=data.get('creator')).first()
        print(f"2 {request.data=}")
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
            permission_classes = [IsCreatorOrOwnerOfBudgetExecution]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

