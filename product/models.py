from django.db import models
from department.models import Departments

# Create your models here.
class Products(models.Model):
    id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField(max_length=255)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
