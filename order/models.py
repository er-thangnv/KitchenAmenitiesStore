from django.db import models
from enum import Enum
from login.models import Accounts
from product.models import Products

# Create your models here.
class Status(Enum):
    WAITING = 'Waiting'
    CANCEL = 'Cancel'
    SUCCESS = 'Success'

class PaymentMethods(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    email = models.CharField(max_length=255)
    note = models.CharField(max_length=1000)
    sub_total = models.FloatField()
    amount = models.IntegerField()
    total = models.FloatField()
    status = models.CharField(max_length=255)
    payment_method = models.ForeignKey(PaymentMethods, on_delete=models.CASCADE)
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class OrderDetails(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

class Payments(models.Model):
    id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    payment_order_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
