from config.enums import CustomEnum
from rest_framework.permissions import BasePermission, IsAuthenticated
from user.models import User


class DjangoViewAction(CustomEnum):
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    RETRIEVE = "retrieve"
    PARTIAL_UPDATE = "partial_update"
    DELETE = "destroy"


class CustomBasePermission(BasePermission):
    allowed_actions = [
        DjangoViewAction.values()
    ]

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_staff:
            return True
        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # print("HERE")
        if (
            request.user.is_staff
            or (isinstance(obj, User) and request.user == obj)
            or (hasattr(obj, "user") and obj.user == request.user)
        ):
            return True
        return False
