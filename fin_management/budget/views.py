from io import BytesIO
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from budget.models import Budget, Funds
from user.models import User
from budget.serializers import BudgetSerializer, FundsSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from config.permissions import IsCreatorOfObject
from budget.permissions import IsCreatorOrOwnerOfBudgetExecution, BudgetPermission, Funds, FundsPermission
from django.http import HttpResponse
from django.db.models import Prefetch
from config.tasks import print_some

class ReportAPIView(APIView):

    def get_permissions(self):
        permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in permission_classes]

    def get(self, request):
        print(f'{request.GET=}')
        id = request.GET.get('id', '')
        data_ = Budget.objects.filter(id=id).first()
        if data_:
            response = HttpResponse(content_type='text/plain')
            response['Content-Disposition'] = 'filename="report.txt"'

            buffer = BytesIO()
            buffer.write(f'Budget: {data_}'.encode('utf-8'))
            data_funds = Funds.objects.filter(budget__pk=id).all()
            for i in data_funds:
                buffer.write(f'\nCreator: {i.creator} sum {i.sum}'.encode('utf-8'))

            txt = buffer.getvalue()
            buffer.close()

            response = HttpResponse(txt, content_type='application/text charset=utf-8')
            response['Content-Disposition'] = 'attachment; filename="report.txt"'
            return response
        else:
            return Response(None, status=status.HTTP_201_CREATED)


class BudgetViewSet(ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    search_fields = ("name", "creator__username", "creator__first_name", "creator__last_name",
                     "creator__email", "sum")
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
        print_some.delay(f'create {serializer.data} for budget')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        data = request.data
        data['creator'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.update(serializer)
        print_some.delay(f'patch {serializer.data} for budget')
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


