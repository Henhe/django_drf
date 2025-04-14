from rest_framework.serializers import ModelSerializer, CharField, ValidationError, Serializer
#, IntegerField, CharField, EmailField
from user.models import User
from django.contrib.auth import authenticate
from config.tasks import print_some

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]


# class UserLoginSerializer(ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["username", "password"]


# class RegisterSerializer(ModelSerializer):
class RegistrationSerializer(ModelSerializer):
    password = CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )
    token = CharField(max_length=255, read_only=True)
    class Meta:
        model = User
        fields = ["username", "password", "email", "token", "password"]

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(Serializer):
    username = CharField(max_length=255, read_only=True)
    password = CharField(max_length=128, write_only=True)
    token = CharField(max_length=255, read_only=True)
    print_some.delay(f'login for user')
    def validate(self, data):
        # В методе validate мы убеждаемся, что текущий экземпляр
        # LoginSerializer значение valid. В случае входа пользователя в систему
        # это означает подтверждение того, что присутствуют адрес электронной
        # почты и то, что эта комбинация соответствует одному из пользователей.
        # email = data.get('email', None)
        username = data.get('username', None)
        password = data.get('password', None)
        print(f'{username=}')
        print(f'{password=}')
        print_some.delay(f'login for user')
        # Вызвать исключение, если не предоставлена почта.
        if username is None:
            raise ValidationError(
                'An username is required to log in.'
            )

        # Вызвать исключение, если не предоставлен пароль.
        if password is None:
            raise ValidationError(
                'A password is required to log in.'
            )

        # Метод authenticate предоставляется Django и выполняет проверку, что
        # предоставленные почта и пароль соответствуют какому-то пользователю в
        # нашей базе данных. Мы передаем email как username, так как в модели
        # пользователя USERNAME_FIELD = email.
        user = authenticate(username=username, password=password)

        # Если пользователь с данными почтой/паролем не найден, то authenticate
        # вернет None. Возбудить исключение в таком случае.
        if user is None:
            raise ValidationError(
                'A user with this email and password was not found.'
            )

        # Django предоставляет флаг is_active для модели User. Его цель
        # сообщить, был ли пользователь деактивирован или заблокирован.
        # Проверить стоит, вызвать исключение в случае True.
        if not user.is_active:
            raise ValidationError(
                'This user has been deactivated.'
            )

        # Метод validate должен возвращать словать проверенных данных. Это
        # данные, которые передются в т.ч. в методы create и update.
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }