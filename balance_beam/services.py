from django.db import transaction
from .models import CustomCustomer, BalanceOperation


class BalanceService:
    @staticmethod
    def _perform_balance_operation(
        user: CustomCustomer,
        amount_in_rubles: float,
        operation_type: str,
        related_customer: CustomCustomer | None = None,
        text_error: str | None = None,
        success: bool = True,
    ) -> BalanceOperation:
        """
        Perform a balance operation for a user and create a corresponding BalanceOperation record.
        Args:
        user (CustomCustomer): The user for whom the balance operation is being performed.
        amount_in_rubles (float): The amount of rubles involved in the operation.
        operation_type (str): The type of the operation.
        related_customer (CustomCustomer, optional): The related customer for the operation.
        text_error (str, optional): The error message, if any.
        success (bool): Indicates if the operation was successful.
        Returns:
        BalanceOperation: The created BalanceOperation record.
        """
        with transaction.atomic():
            user = CustomCustomer.objects.select_for_update().get(pk=user.pk)
            if not text_error:
                user.balance += amount_in_rubles
                user.save()
            operation = BalanceOperation.objects.create(
                user=user,
                amount=amount_in_rubles,
                operation_type=operation_type,
                text_error=text_error,
                related_customer=f"{related_customer.email}, id: {related_customer.id}"
                if related_customer
                else None,
                success=success,
            )
        return operation

    @classmethod
    def increase_balance(
        cls, user: CustomCustomer, amount_in_kopecks: int, sender: CustomCustomer = None
    ) -> BalanceOperation:
        """
        Increase the balance of the user by the specified amount.
        Args:
            user (User): The user whose balance will be increased.
            amount_in_kopecks (int): The amount to increase the balance, in kopecks.
            sender (User, optional): The sender of the increase balance operation.
        Returns:
            BalanceOperation: The balance operation object representing the increase.
        """
        amount_in_rubles = amount_in_kopecks
        return cls._perform_balance_operation(
            user, amount_in_rubles, "INCREASE", related_customer=sender
        )

    @classmethod
    def decrease_balance(
        cls,
        user: CustomCustomer,
        amount_in_kopecks: int,
        recipient: CustomCustomer | None = None,
    ) -> BalanceOperation:
        """
        Decreases the balance of the user by the specified amount and performs a transfer operation.
        Args:
        - user: The user whose balance will be decreased.
        - amount_in_kopecks: The amount to decrease the balance in kopecks.
        - recipient: The recipient of the transfer operation.
        Returns:
        - BalanceOperation: The balance operation object representing the transfer.
        """
        amount_in_rubles = amount_in_kopecks
        return cls._perform_balance_operation(
            user, -amount_in_rubles, "TRANSFER", related_customer=recipient
        )

    @staticmethod
    def check_user_balance_in_kopecks(user: CustomCustomer) -> int:
        """Get the user's balance in kopecks.
        Args:
            user (CustomCustomer): The custom customer object.
        Returns:
            int: The user's balance in kopecks.
        """
        return user.balance

    @staticmethod
    def check_user_balance_in_rubles(user: CustomCustomer) -> float | None:
        """Check user balance in rubles

        Args:
            user (CustomCustomer): The user object

        Returns:
            Optional[float]: The user balance in rubles, or None if user object is not valid
        """
        if user is None:
            return None
        return user.balance / 100

    @classmethod
    def transfer_balance(
        cls, sender: CustomCustomer, recipient_id: int, amount_in_kopecks: int
    ) -> int:
        """
        Transfer balance from one customer to another.

        Args:
            sender (CustomCustomer): The customer sending the money.
            recipient_id (int): The ID of the recipient customer.
            amount_in_kopecks (int): The amount to be transferred in kopecks.

        Returns:
            Decimal: The remaining balance of the sender after the transfer.
        """
        with transaction.atomic():
            sender_customer = CustomCustomer.objects.select_for_update().get(
                pk=sender.pk
            )
            recipient_customer = CustomCustomer.objects.select_for_update().get(
                pk=recipient_id
            )
            if sender_customer == recipient_customer:
                error_message = "You can't transfer money to yourself. Please choose another recipient."
                cls._perform_balance_operation(
                    sender_customer,
                    -amount_in_kopecks,
                    "DECREASE",
                    text_error=error_message,
                    related_customer=recipient_customer,
                    success=False,
                )
                raise ValueError(error_message)
            if sender_customer.balance < amount_in_kopecks:
                error_message = f"Insufficient balance. User balance: {sender_customer.balance / 100} rubles"
                cls._perform_balance_operation(
                    sender_customer,
                    -amount_in_kopecks,
                    "DECREASE",
                    text_error=error_message,
                    related_customer=sender_customer,
                )
                raise ValueError(error_message)
            cls.decrease_balance(
                sender_customer, amount_in_kopecks, recipient=recipient_customer
            )
            cls.increase_balance(
                recipient_customer, amount_in_kopecks, sender=sender_customer
            )

        return sender_customer.balance

    @staticmethod
    def get_last_operations(
        user: CustomCustomer, limit: int = 5
    ) -> list[BalanceOperation]:
        """Retrieve data about the user's last operations."""
        operations: list[BalanceOperation] = BalanceOperation.objects.filter(
            user=user
        ).order_by("-timestamp")[:limit]
        return operations
