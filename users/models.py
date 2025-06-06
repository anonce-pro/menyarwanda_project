from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Add additional fields here if needed in the future
    is_subscriber = models.BooleanField(default=False)

    def __str__(self):
        return self.username

