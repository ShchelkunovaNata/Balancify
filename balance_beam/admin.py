from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _
from rest_framework.request import Request

from .models import CustomCustomer, BalanceOperation
from .common import admin_site


@admin.register(CustomCustomer, site=admin_site)
class CustomCustomerAdmin(DjangoUserAdmin):
    """Административный интерфейс модели User.

    В модели нет поля `username`. Поэтому здесь переопределяются все
    атрибуты, где оно фигурирует.
    """

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        (
            _("Personal info"),
            {
                "fields": [
                    "first_name",
                    "last_name",
                    "phone",
                    "birth_date",
                    "balance",
                ]
            },
        ),
        (
            _("Permissions"),
            {
                "fields": [
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ]
            },
        ),
    ]
    add_fieldsets = [
        (
            None,
            {
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "balance",
                ]
            },
        ),
    ]
    readonly_fields = ["last_login", "date_joined", "balance"]
    list_display = ["email", "first_name", "last_name", "balance"]
    list_filter = [
        "is_staff",
        "is_superuser",
        "is_active",
    ]
    search_fields = ["first_name", "last_name", "email", "phone"]
    ordering = ["-date_joined", "-id"]


@admin.register(BalanceOperation, site=admin_site)
class BalanceOperationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "related_customer",
        "amount",
        "operation_type",
        "timestamp",
        "success",
    )
    list_filter = ("operation_type", "timestamp", "success")
    search_fields = ("user__email", "related_customer")

    def get_queryset(self, request: Request) -> QuerySet:
        """Override for query optimization. Returns the queryset with 'user' relationship pre-fetched."""
        queryset = super().get_queryset(request)
        return queryset.select_related("user")
