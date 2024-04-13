from enum import Enum

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from users.manager import UserManager


class UserType(Enum):
    admin = 'ADMIN'
    regular = 'REGULAR'

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=11, unique=True)
    user_type = models.CharField(choices=UserType.choices, default=UserType.regular.value, max_length=7)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username', 'password']

    objects = UserManager()

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username
