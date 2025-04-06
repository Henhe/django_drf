from category.views import CategoryViewSet#, TokenAuthView, RegisterView, UserContactViewSet
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("", CategoryViewSet)

urlpatterns = [
] + router.urls