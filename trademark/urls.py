from django.urls import path
from . import views

urlpatterns = [
    path('trademarks/', views.get_trademarks, name='trademarks'),
]