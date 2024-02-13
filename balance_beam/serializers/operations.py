from rest_framework import serializers
from ..models import BalanceOperation, CustomCustomer
from django.shortcuts import get_object_or_404


class BalanceIncreaseOperationSerializer(serializers.ModelSerializer):
    operation_type = serializers.CharField(default="INCREASE")

    class Meta:
        model = BalanceOperation
        fields = ["amount", "operation_type", "timestamp", "success", "text_error"]

    @staticmethod
    def validate_amount(value: int) -> int:
        """Validate that the amount is a positive number.
        Args:
        value (int): The amount to be validated.
        Returns:
        int: The validated amount.
        """
        if value is None:
            raise serializers.ValidationError("Amount cannot be None.")
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value


def validate_recipient_id(value: int) -> int:
    """Validate that the user_id exists in the database."""
    CustomCustomer.objects.get(id=value)
    get_object_or_404(CustomCustomer, id=value)
    return value


class BalanceTransferOperationSerializer(serializers.ModelSerializer):
    operation_type = serializers.CharField(default="DECREASE")
    recipient_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = BalanceOperation
        fields = ["amount", "operation_type", "timestamp", "success", "text_error", "recipient_id"]

    @staticmethod
    def validate_amount(value: int) -> int:
        """Validate that the amount is a positive number.
        Args:
        value (float): The amount to be validated.
        Returns:
        float: The validated amount.
        """
        if value is None:
            raise serializers.ValidationError("Amount cannot be None.")
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
