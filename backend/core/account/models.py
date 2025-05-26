from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionMixin)

class User(AbstractBaseUser, PermissionMixin):
    email = models.EmailField(max_length = 255, unique = True)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    created_date = models.DateTimeField(auto_now_add = True)
    updated_date = models.DateTimeField(auto_now = True)

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
