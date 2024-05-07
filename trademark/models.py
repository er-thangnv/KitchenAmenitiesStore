from django.db import models

# Create your models here.
class Trademarks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    link_info = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
