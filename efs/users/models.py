from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_name = models.CharField (max_length=50, default=' ', null=True, blank=True)
    email = models.CharField(max_length=50, default=' ', null=True, blank=True)
    first_name = models.CharField(max_length=50, default=' ', null=True, blank=True)
    last_name = models.CharField(max_length=50, default=' ', null=True, blank=True)