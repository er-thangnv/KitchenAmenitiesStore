from django.shortcuts import render
from rest_framework.decorators import api_view
from product.models import Products
from django.shortcuts import redirect
from login.models import Accounts

# Create your views here.
@api_view(['GET'])
def checkout(request, id): 
    if request.session.get("current_user_id") is None:
        return redirect('/KitchenAmenitiesStore/login/')
    else:
        current_user_id = request.session.get("current_user_id")
        account = Accounts.objects.get(id=current_user_id)
        product = Products.objects.get(id=id)
        context = {
            'product': {
                'id': id,
                'name': product.name,
                'price': product.price
            }
        }
        context['account'] = account
        return render(request, 'checkout.html', context)
