from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from config.models import Timestamp
from enum import Enum


class UserRole(Enum):
    USER = 1
    ADMIN = 2


class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            username,
            password=None,
            first_name="",
            last_name="",
            is_active=False,

    ):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            username=username
        )
        user.set_password(password)
        user.role = UserRole.USER.value
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            email,
            username,
            password=None,

    ):
        print(email)
        user = self.create_user(
            email=email,
            is_active=True,
            username=username,
            password=password,
        )
        user.role = UserRole.ADMIN.value
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, Timestamp, models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(default=UserRole.USER.value)
    # contacts = models.ManyToManyField(
    #     "User",
    #     through="UserContact",
    #     through_fields=("user", "contact")
    # )

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username

    # @property
    # def is_staff(self):
    #     return self.role == UserRole.ADMIN.value

