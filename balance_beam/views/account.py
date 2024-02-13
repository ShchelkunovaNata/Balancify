from rest_framework import mixins, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from ..serializers import (
    UserSerializer,
    UserSerializerForUpdate
)
from ..models import CustomCustomer


class UserViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """Управление сущностью Customer (Пользователь).

    Процесс регистрации пользователей, обновление профиля.
    """

    queryset = CustomCustomer.objects.all()
    serializer_class = UserSerializer

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Create a new instance of the resource.
        Args:
        - request (Request): The request object containing the data for the new instance.
        - *args (Any): Additional positional arguments.
        - **kwargs (Any): Additional keyword arguments.

        Returns:
        - Response: The response containing the new instance and a status code.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.instance, status=status.HTTP_201_CREATED)

    def get_serializer_class(self) -> UserSerializer | UserSerializerForUpdate:
        """
        Return the appropriate serializer class based on the request method.
        Args:
            self: The instance of the class.
        Returns:
            Type[Serializer]: The appropriate serializer class for the request method.
        """
        serializer_class = self.serializer_class

        if self.request.method in ("PUT", "PATCH"):
            serializer_class = UserSerializerForUpdate

        return serializer_class

    def update(self, request: Request, *args: Any, **kwargs: Any) -> Any:
        """
        Update function with permission check.

        Args:
        - request: The request object.
        - args: Additional positional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - The updated object.
        """
        if int(kwargs["pk"]) != request.user.id:
            raise PermissionError(
                """Insufficient permissions to perform this action."""
            )

        return super().update(request, *args, **kwargs)

    def current(self, request: Request) -> Response:
        """Get current user data.
        Retrieve data about the authenticated user.

        Args:
            request (Request): The request object.
        Returns:
            Response: The response object containing user data.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

