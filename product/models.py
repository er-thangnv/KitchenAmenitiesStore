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

    def __str__(self):
        return f"{self.name}"

class DescriptionsProduct(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=255)
    image1 = models.CharField(max_length=255)
    image2 = models.CharField(max_length=255)
    image3 = models.CharField(max_length=255)
    image4 = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.product.name}"
