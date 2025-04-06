from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from config.models import Timestamp
from enum import Enum
from django.contrib.auth.models import PermissionsMixin
from datetime import datetime, timedelta
from config import settings
import jwt

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
        user = self.create_user(
            email=email,
            is_active=True,
            username=username,
            password=password,
        )
        user.role = UserRole.ADMIN.value
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, Timestamp, PermissionsMixin):
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
        return f'{self.username} is staff {self.is_staff} id-{self.id}'

    @property
    def is_staff(self):
        return self.role == UserRole.ADMIN.value

    @property
    def is_superuser(self):
        return self.role == UserRole.ADMIN.value

    # @property
    # def token(self):
    #     """
    #     Позволяет получить токен пользователя путем вызова user.token, вместо
    #     user._generate_jwt_token(). Декоратор @property выше делает это
    #     возможным. token называется "динамическим свойством".
    #     """
    #     return self._generate_jwt_token()
    #
    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя, срок действия токена составляет 1 день от создания
    #     """
    #     dt = datetime.now() + timedelta(days=1)
    #
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     return token.decode('utf-8')

    # @property
    # def token(self):
    #     """
    #     Позволяет получить токен пользователя путем вызова user.token, вместо
    #     user._generate_jwt_token(). Декоратор @property выше делает это
    #     возможным. token называется "динамическим свойством".
    #     """
    #     return self._generate_jwt_token()
    #
    # def _generate_jwt_token(self):
    #     """
    #     Генерирует веб-токен JSON, в котором хранится идентификатор этого
    #     пользователя, срок действия токена составляет 1 день от создания
    #     """
    #     dt = datetime.now() + timedelta(days=1)
    #     # print(f'{dt.strftime('%s')=}')
    #
    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int((dt - datetime(1, 1, 1, 0, 0)).total_seconds())
    #     }, settings.SECRET_KEY, algorithm='HS256')
    #
    #     return token.decode('utf-8')