from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('auth/login/', views.handler_login, name='handler_login'),
]