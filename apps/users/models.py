from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.base.models import TimeStampModel
from apps.users.managers import UserManager


class User(TimeStampModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for the application.

    Attributes:
        email (str): Unique email address used for authentication.
        first_name (str): User's first name.
        last_name (str): User's last name (optional).
        phone_number (str): Contact number (optional).
        is_active (bool): Indicates whether the user account is active.
        is_staff (bool): Indicates whether the user can access Django admin.

    This model uses email as the unique login identifier
    and integrates with Django's authentication and
    permisssion system.
    """

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # Field used for authentication
    USERNAME_FIELD = "email"

    # Fields required when creating a superuser
    REQUIRED_FIELDS = ["first_name"]

    def __str__(self):
        """
        String representation of the user.
        Used in Django admin and logs.
        """
        return self.email
