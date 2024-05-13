from django.contrib import admin
from .models import PaymentMethods, Orders

# Register your models here.
admin.site.register(PaymentMethods)
admin.site.register(Orders)