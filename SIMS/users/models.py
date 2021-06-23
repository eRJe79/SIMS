from django.db import models
from django.contrib.auth.models import AbstractUser

# Defining types of users
class User(AbstractUser):
    is_main_user = models.BooleanField(default=False) # Franck's account
    is_lambda = models.BooleanField(default=False) # user with read only rights
    is_admin = models.BooleanField(default=False) # admin account

