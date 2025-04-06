from config.enums import CustomEnum
from rest_framework.permissions import BasePermission, IsAuthenticated
from user.models import User


class IsOwnerOfObject(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.is_staff:
            return True
        if view.action in self.allowed_actions:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj == request.user


class IsCreatorOfObject(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.creator == request.user


class DjangoViewAction(CustomEnum):
    LIST = "list"
    CREATE = "create"
    UPDATE = "update"
    RETRIEVE = "retrieve"
    PARTIAL_UPDATE = "partial_update"
    DELETE = "destroy"


class CustomBasePermission(BasePermission):
    allowed_actions = DjangoViewAction.values()

