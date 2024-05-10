"""
URL configuration for my_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('KitchenAmenitiesStore/', include('register.urls')),
    path('KitchenAmenitiesStore/', include('login.urls')),
    path('KitchenAmenitiesStore/', include('home.urls')),
    path('KitchenAmenitiesStore/', include('product.urls')),
    path('KitchenAmenitiesStore/', include('checkout.urls')),
    path('KitchenAmenitiesStore/', include('order.urls')),
    path('api/v1/', include('register.urls')),
    path('api/v1/', include('login.urls')),
    path('api/v1/', include('department.urls')),
    path('api/v1/', include('trademark.urls')),
    path('api/v1/', include('user.urls')),
    path('api/v1/', include('product.urls')),
    path('api/v1/', include('order.urls')),
]
