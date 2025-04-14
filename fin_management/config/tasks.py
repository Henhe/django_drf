from celery import shared_task, Celery

from celery.utils import log

app = Celery('tasks', broker='amqp://myuser:mypassword@localhost:5672/myvhost')

@shared_task
def print_some(txt):
    print(f"{txt}")


@shared_task
def change_users_is_active_task():
    pass
    # names = ["John", "Bob", "Jeff", "Some name"]
    # log.task_logger.log(1, f"Running user update task")
    # users_to_change = User.objects.filter(role=UserRole.REGULAR.value).all()
    # for user in users_to_change:
    #     user.is_active = bool(not user.is_active)
    #     user.first_name = random.choice(names)
    #     user.save()

