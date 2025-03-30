from rest_framework.serializers import ModelSerializer #, IntegerField, CharField, EmailField
from budget.models import Budget


class BudgetSerializer(ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'


