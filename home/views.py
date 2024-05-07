from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template import loader
from django.http import HttpResponse
from login.models import Accounts

# Create your views here.
def home(request):
    current_user_id = request.session.get("current_user_id")
    if current_user_id is None:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())
    account = Accounts.objects.get(id=current_user_id)
    if account is None:
        template = loader.get_template('home.html')
        return HttpResponse(template.render())
    else:
        context = {
        'account': account, 
        }
        return render(request, 'home.html', context)
