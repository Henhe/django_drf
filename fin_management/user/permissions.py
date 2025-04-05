from config.permissions import CustomBasePermission
from config.permissions import DjangoViewAction


class UserPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values(exclude=[DjangoViewAction.CREATE])



