from rest_framework import routers
from django.urls import path
from .views import (
    increase_balance,
    check_balance,
    check_balance_in_rubles,
    get_operations_history,
    transfer_balance,
    UserViewSet,
)


__all__ = ["urlpatterns"]

router = routers.DefaultRouter(trailing_slash=False)

router.register("account", UserViewSet, basename="users")

urlpatterns = router.urls + [
    path("increase_balance/", increase_balance, name="increase_balance"),
    path("check_balance/", check_balance, name="check_balance"),
    path(
        "check_balance_in_rubles/",
        check_balance_in_rubles,
        name="check_balance_in_rubles",
    ),
    path(
        "get_operations_history/", get_operations_history, name="get_operations_history"
    ),
    path("transfer_balance/", transfer_balance, name="transfer_balance"),
]
