from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=128)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
