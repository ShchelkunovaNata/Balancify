from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomerManager(DjangoUserManager):
    """Менеджер пользователей.

    Собственный менеджер пользователей учитывает рекомендации Django по
    заведению новых пользователей сайта.
    https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    """

    def create_user(
        self, email: str, password: str | None = None, **kwargs
    ) -> "CustomCustomer":
        """
        Creates a new user with the given email and optional password, and saves it to the database.

        Parameters:
            email (str): The email address of the user.
            password (str | None): The password for the user. Defaults to None.
            **kwargs: Additional keyword arguments to pass to the user model.

        Returns:
            CustomCustomer: The newly created user object.
        """
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email, password=None, **kwargs
    ):  # pylint: disable=arguments-differ
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        return self.create_user(email, password, **kwargs)


# Валидация учитывает и различные странные Имена, Фамилии по типу: Хун'ы Ю Я
validate_names = RegexValidator(
    r"^[A-ZÀ-ÿА-ЯЁ][a-zà-ÿа-яё]*(([^\S\n\t]?(\'|\’|-|[^\S\n\t])[^\S\n\t]?)([A-ZÀ-ÿА-ЯЁ]?[a-zà-ÿа-яё])+)*$",
    _("alphabetic values, apostrophes, hyphens are allowed"),
)


# Валидатор номера телефона учитывает только международный формат.
validate_phone = RegexValidator(
    r"^7[^6,7]\d{9,15}$",
    _(
        "Incorrect phone number format. \
    Please enter a Russian phone number using numbers only"
    ),
)


class CustomCustomer(AbstractUser):
    """Модель User.

    Любой пользователь сайта (в т.ч. админки). Здесь переопределяются поля по
    нашим требованиям: имя пользователя не учитывается, авторизация происходит
    по электронной почте, личное имя и фамилия обязательны. Остальное пусть будет как заглушка для имитации
    полноценного функционала
    """

    username = None
    first_name = models.CharField(
        _("first name"), max_length=150, validators=[validate_names]
    )
    last_name = models.CharField(
        _("last name"), max_length=150, validators=[validate_names]
    )
    email = models.EmailField(
        _("email address"), unique=True
    )  # не требует доп. валидаций
    email_verification_status = models.BooleanField(
        _("email verification status"), default=False
    )
    balance = models.PositiveIntegerField(default=0)
    phone = models.CharField(
        _("telephone number"),
        max_length=15,
        validators=[validate_phone],
        unique=True,
        help_text=_("Only numbers in the international format E.164."),
        blank=True,
        null=True,
    )
    birth_date = models.DateField(null=True, blank=True)

    objects = CustomerManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
