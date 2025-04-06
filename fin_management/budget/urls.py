from budget.views import BudgetViewSet, FundsViewSet, ReportAPIView
from rest_framework.routers import SimpleRouter
from django.urls import path


router = SimpleRouter()
router.register("", BudgetViewSet, basename='budget')
# router.register("funds", FundsViewSet, basename='fund')

urlpatterns = [
    path("funds/", FundsViewSet.as_view({'get':'list', 'post':'create'}), name="fund"),
    path("report/", ReportAPIView.as_view(), name="report"),
] + router.urls

