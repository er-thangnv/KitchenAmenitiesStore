from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.get_departments, name='departments'),
]