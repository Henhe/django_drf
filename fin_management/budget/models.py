from django.db import models
from user.models import User

from config.models import Timestamp

class Budget(Timestamp, models.Model):
    name = models.CharField(unique=True, max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_budgets")
    sum = models.FloatField()