from django.urls import path
from . import views

urlpatterns = [
    path('orders', views.create_order, name='create_order'),
    path('orders/<str:payment_order_id>/capture', views.capture_order, name='capture_order'),
]