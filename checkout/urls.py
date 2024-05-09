from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:id>', views.checkout, name='checkout'),
]