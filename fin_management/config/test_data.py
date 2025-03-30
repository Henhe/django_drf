import os
import django
import random
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from user.models import User
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


# def generate_house(number):
#     seeder = Seed.seeder()
#
#     seeder.add_entity(House, number, {
#         'created_at': lambda x: seeder.faker.date(),
#         'updated_at': lambda x: seeder.faker.date(),
#         'title': lambda x: seeder.faker.address()[:150],
#         'description': lambda x: seeder.faker.text(),
#         'square': lambda x: seeder.faker.random_int(),
#         'owner': lambda x: random.choice(CustomUser.objects.filter(role="saler")),
#         'status': lambda x: 'free',
#     })
#
#     seeder.execute()


if __name__ == "__main__":
    generate_users(40)
    # generate_house(100)
