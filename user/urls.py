from django.urls import path
from . import views

urlpatterns = [
    path('users/current', views.get_user_current, name='get_user_current'),
    path('users/log-out', views.log_out, name='log_out'),
]