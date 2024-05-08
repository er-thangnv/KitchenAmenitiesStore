from django.urls import path
from . import views

urlpatterns = [
    path('products/new', views.get_new_products, name='new_products'),
]