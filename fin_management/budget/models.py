from django.db import models
from user.models import User

from config.models import Timestamp

class Budget(Timestamp, models.Model):
    name = models.CharField(unique=True, max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_budgets")
    sum = models.FloatField()

    def __str__(self):
        return f'{self.name} ({self.creator}) - {self.sum}'


class BudgetExecution(Timestamp, models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="budget_executions")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_budget_executions")
    sum = models.FloatField()
