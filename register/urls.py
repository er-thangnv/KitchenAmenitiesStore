from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('auth/register/', views.handler_register, name='handler_register'),
]