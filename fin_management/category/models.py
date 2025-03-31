from django.db import models
# from user import User

from config.models import Timestamp

from user.models import User


class Category(Timestamp, models.Model):
    name = models.CharField(unique=True, max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_creators")

    def __str__(self):
        return f'{self.name} ({self.creator})'
