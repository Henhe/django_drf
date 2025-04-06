from config.permissions import CustomBasePermission
from config.permissions import DjangoViewAction
from rest_framework.permissions import BasePermission
from budget.models import Funds

class BudgetPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()


class FundsPermission(CustomBasePermission):
    allowed_actions = DjangoViewAction.values()


class IsCreatorOrOwnerOfBudgetExecution(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        if (isinstance(obj, Funds) and obj.budget.creator == request.user
                or obj.creator == request.user):
            return True
        return False
        # return obj.creator == request.user


