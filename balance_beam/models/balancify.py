from django.db import models
from ..models import CustomCustomer


class BalanceOperation(models.Model):
    user = models.ForeignKey(
        CustomCustomer, on_delete=models.PROTECT, related_name="balance_operations"
    )
    related_customer = models.CharField(max_length=255, null=True, blank=True)
    amount = models.IntegerField()
    OPERATION_TYPES = (
        ("INCREASE", "Increase"),
        ("TRANSFER", "Transfer"),
    )
    operation_type = models.CharField(max_length=8, choices=OPERATION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    text_error = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        """Return a string representation of the operation."""
        return f"Operation {self.operation_type} for {self.user} in {self.timestamp} datetime"
