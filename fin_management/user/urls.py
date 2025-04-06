from user.views import UserViewSet#, LoginAPIView, RegistrationAPIView #, TokenAuthView, RegisterView, UserContactViewSet
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("", UserViewSet)

urlpatterns = [
] + router.urls