from django.urls import path
from . import views

urlpatterns = [
    path('products/new', views.get_new_products, name='new_products'),
    path('products', views.get_all_products, name='all_products'),
    path('products/<int:id>', views.get_details_product, name='product_detail'),
]