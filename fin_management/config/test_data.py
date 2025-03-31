import os
import django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from user.models import User
from category.models import Category
from budget.models import Budget

from django_seed import Seed
from django.utils import timezone


def generate_users(number):
    seeder = Seed.seeder()

    seeder.add_entity(User, number, {
        'first_name': lambda x: seeder.faker.first_name(),
        'last_name': lambda x: seeder.faker.last_name(),
        'email': lambda x: seeder.faker.email(),
        'username': lambda x: seeder.faker.user_name(),
        # 'date_joined': timezone.now(),
        # 'last_login': timezone.now(),
    })

    seeder.execute()


def generate_category(number):
    seeder = Seed.seeder()

    seeder.add_entity(Category, number, {
        'created_at': lambda x: seeder.faker.date(),
        'updated_at': lambda x: seeder.faker.date(),
        'name': lambda x: seeder.faker.text(),
        'creator': lambda x: random.choice(User.objects.all()),
    })

    seeder.execute()

def generate_budget(number):
    seeder = Seed.seeder()

    seeder.add_entity(Budget, number, {
        'created_at': lambda x: seeder.faker.date(),
        'updated_at': lambda x: seeder.faker.date(),
        'name': lambda x: seeder.faker.text(),
        'creator': lambda x: random.choice(User.objects.all()),
        'sum': lambda x: seeder.faker.random_int(),
    })

    seeder.execute()

if __name__ == "__main__":
    generate_users(5)
    # generate_category(30)
    # generate_budget(20)
