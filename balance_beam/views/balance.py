from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from ..services import BalanceService
from ..serializers import (
    HistoryOperationSerializer,
    BalanceIncreaseOperationSerializer,
    BalanceTransferOperationSerializer,
)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def increase_balance(request: Request) -> Response:
    """
    Increase user balance based on the amount provided in kopecks.

    Args:
        request: HttpRequest object

    Returns:
        Response: Response object containing the result of the increase operation
    """
    user = request.user
    serializer = BalanceIncreaseOperationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data
    amount_in_kopecks = validated_data.get("amount")
    BalanceService.increase_balance(
        user, amount_in_kopecks=amount_in_kopecks, sender=user
    )
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def check_balance(request: Request) -> Response:
    """
    Retrieve the user's balance in kopecks.
    Args:
        request (Request): The incoming request object.
    Returns:
        Response: A JSON response containing the user's balance in kopecks.
    """
    user = request.user
    balance = BalanceService.check_user_balance_in_kopecks(user)
    return Response({"balance": f"{balance} in kopecks"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def check_balance_in_rubles(request: Request) -> Response:
    """
    Check the user's balance in rubles.
    Args:
        request (Any): The request object.
    Returns:
        Response: The JSON response containing the user's balance in rubles.
    """
    user = request.user
    balance = BalanceService.check_user_balance_in_rubles(user)
    return Response({"balance": f"{balance} rubles"})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_operations_history(request: Request) -> Response:
    """
    Retrieve the last operations history for the authenticated user.
    Args:
        request (Request): The request object containing user information.
    Returns:
        Response: The response object containing the serialized history operations data.
    """
    # TODO: хотелось ещё подзаморочиться и сделать разные параметры для фильтрации, но я уже и так наделала делов)
    user = request.user
    history = BalanceService.get_last_operations(user)
    serializer = HistoryOperationSerializer(history, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def transfer_balance(request: Request) -> Response:
    """
    Transfer balance from the user's account to another user's account.

    Args:
    - request: Request object containing user data and transfer details

    Returns:
    - Response: Response object with current balance or error message
    """

    user = request.user

    serializer = BalanceTransferOperationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated_data = serializer.validated_data

    try:
        user_balance = BalanceService.transfer_balance(
            user,
            amount_in_kopecks=validated_data.get("amount"),
            recipient_id=validated_data.get("recipient_id"),
        )
    except ValueError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {
            "current_balance": f"{user_balance} in kopecks",
        },
        status=status.HTTP_200_OK,
    )
