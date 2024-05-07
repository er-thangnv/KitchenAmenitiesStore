from django.db import models
from enum import Enum

# Create your models here.
class RoleEnum(Enum):
    USER = 'user'
    ADMIN = 'admin'

class Accounts(models.Model):
    id = models.UUIDField(primary_key=True)
    email = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=10, choices=[(role.value, role.name) for role in RoleEnum], default=RoleEnum.USER.value)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
