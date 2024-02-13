from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from ..models import validate_names, validate_phone, CustomCustomer
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as RestValidationError


def validate_number_phone(phone: str) -> None:
    """
    Validate the phone number.
    Args:
    phone (str): The phone number to be validated.
    Raises:
    RestValidationError: If the phone number is not valid.
    """
    try:
        validate_phone(phone)
    except ValidationError:
        raise RestValidationError(
            _("Number must be no more than 15 digits, without + .")
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomCustomer
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "birth_date",
            "balance",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False},
            "phone": {"required": False},
            "last_name": {"required": False},
            "birth_date": {"required": False},
            "balance": {"read_only": True},
        }

    def create(self, validated_data: dict[str, str | int]) -> dict[str, bool]:
        """
        Create a new CustomCustomer object using the validated data.
        Args:
        - validated_data (dict): The data to be used for creating the CustomCustomer object.
        Returns:
        - dict: A dictionary indicating the success of the operation.
        """
        instance = CustomCustomer()

        try:
            password_validation.validate_password(
                validated_data.get("password"), instance
            )
        except ValidationError as error:
            raise serializers.ValidationError({"password": error.messages})

        if "phone" in validated_data:
            validate_number_phone(validated_data.get("phone"))
        try:
            CustomCustomer.objects.create(**validated_data)
        except Exception as error:
            raise serializers.ValidationError({"error": error})
        return {"success": True}


class UserExistsSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class UserSerializerForUpdate(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomCustomer
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "birth_date",
            "phone",
            "old_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
            "birth_date": {"required": False},
            "email": {"read_only": True},
            "balance": {"read_only": True},
        }

    def update(
        self, instance: CustomCustomer, validated_data: dict[str, str | int]
    ) -> CustomCustomer:
        """
        Update method to modify user instance with validated data.
        Args:
            self: The instance of the class.
            instance: The user instance to be updated.
            validated_data: The validated data to update the user instance.
        Returns:
            The updated user instance.
        """
        if "password" in validated_data:
            if not instance.check_password(validated_data.get("old_password")):
                raise serializers.ValidationError(
                    {"old_password": _("Old password is not correct")}
                )
            try:
                password_validation.validate_password(
                    validated_data.get("password"), instance
                )
            except ValidationError as error:
                raise serializers.ValidationError({"password": error.messages})
            vdata = validated_data
            if vdata.get("old_password") == vdata.get("password"):
                raise serializers.ValidationError(
                    {
                        "password": _(
                            "The new password must be different from the old one"
                        )
                    }
                )

            instance.set_password(validated_data.pop("password"))

        if "first_name" in validated_data:
            try:
                validate_names(validated_data.get("first_name"))
            except ValidationError as error:
                raise serializers.ValidationError({"first_name": error.messages})
            instance.first_name = validated_data.pop("first_name")

        if "last_name" in validated_data:
            try:
                validate_names(validated_data.get("last_name"))
            except ValidationError as error:
                raise serializers.ValidationError({"last_name": error.messages})
            instance.last_name = validated_data.pop("last_name")

        if "phone" in validated_data:
            validate_number_phone(validated_data.get("phone"))

        instance = super().update(instance, validated_data)

        return instance
