from user.views import UserViewSet#, LoginAPIView, RegistrationAPIView #, TokenAuthView, RegisterView, UserContactViewSet
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("", UserViewSet)
# router_contacts = SimpleRouter()
# router.register("contacts", UserContactViewSet)

urlpatterns = [
    # path("token-auth/", TokenAuthView.as_view(), name="token-auth"),
    # path("register/", RegistrationAPIView.as_view(), name="register"),
    # path('login/', LoginAPIView.as_view(), name="login"),
] + router.urls