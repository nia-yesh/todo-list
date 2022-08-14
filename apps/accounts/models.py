from django.db import models
from django.contrib.auth.models import AbstractUser

from utils.enums import UserRole


class User(AbstractUser):
    role = models.PositiveIntegerField(choices=UserRole.choices)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
