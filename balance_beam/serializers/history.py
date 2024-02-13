from rest_framework import serializers
from ..models import BalanceOperation


class HistoryOperationSerializer(serializers.ModelSerializer):

    class Meta:
        model = BalanceOperation
        fields = ["user", "amount", "operation_type", "timestamp", "success", "text_error"]
