from django.urls import path
from . import views

urlpatterns = [
    path('departments/', views.get_departments, name='departments'),
    path('departments/<int:department_id>', views.get_products_by_department, name='get_products_by_department'),
]