from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template import loader
from django.http import HttpResponse
from login.models import Accounts
from product.models import Products

# Create your views here.
def home(request):
    current_user_id = request.session.get("current_user_id")
    new_products = Products.objects.order_by('-created_at')[:6]
    context = {
        'new_products': new_products
    }
    if current_user_id is None:
        return render(request, 'home.html', context)
    account = Accounts.objects.get(id=current_user_id)
    if account is None:
        return render(request, 'home.html', context)
    else:
        context['account'] = account
        return render(request, 'home.html', context)
