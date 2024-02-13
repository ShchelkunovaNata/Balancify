from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from ..serializers import (
    UserSerializer,
    UserExistsSerializer,
    UserSerializerForUpdate
)
from rest_framework.decorators import action
from ..models import CustomCustomer
from rest_framework.permissions import IsAuthenticated, AllowAny



class UserViewSet(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet
):
    """Управление сущностью Customer (Пользователь).

    Процесс регистрации пользователей, обновление профиля.
    """

    queryset = CustomCustomer.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.instance, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        serializer_class = self.serializer_class

        if self.request.method in ("PUT", "PATCH"):
            serializer_class = UserSerializerForUpdate

        return serializer_class

    def update(self, request, *args, **kwargs):
        if int(kwargs["pk"]) != request.user.id:
            raise PermissionError(
                """Недостаточно прав для выполнения данного действия."""
            )

        return super().update(request, *args, **kwargs)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def current(self, request):
        """Текущий пользователь.

        Получить данные о аутентифицированном пользователе.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
    )
    def exists(self, request):
        serialize = UserExistsSerializer(data=request.data)
        serialize.is_valid(raise_exception=True)
        result = {"exists": False, "email_verification_status": False}
        try:
            user = CustomCustomer.objects.get(email=serialize.validated_data["email"])
        except CustomCustomer.DoesNotExist:
            return Response(result)

        result["exists"] = True
        result["email_verification_status"] = user.email_verification_status
        return Response(result)
