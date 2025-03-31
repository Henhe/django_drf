from config.permissions import CustomBasePermission
from config.permissions import DjangoViewAction


class CategoryPermission(CustomBasePermission):
    allowed_actions = [DjangoViewAction.values()]



