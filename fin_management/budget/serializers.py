from rest_framework.serializers import ModelSerializer #, IntegerField, CharField, EmailField
from budget.models import Budget, Funds


class BudgetSerializer(ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


class FundsSerializer(ModelSerializer):
    class Meta:
        model = Funds
        fields = '__all__'
