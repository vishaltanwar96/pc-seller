from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from users.managers import UserManager


class User(AbstractUser):

    last_login = None
    username = None

    objects = UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={'unique': 'A user with this email already exists'}
    )
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
