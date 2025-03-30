from budget.views import BudgetViewSet#, TokenAuthView, RegisterView, UserContactViewSet
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("", BudgetViewSet)
# router_contacts = SimpleRouter()
# router.register("contacts", UserContactViewSet)

urlpatterns = [
    # path("token-auth/", TokenAuthView.as_view(), name="token-auth"),
    # path("register/", RegisterView.as_view(), name="register"),
] + router.urls