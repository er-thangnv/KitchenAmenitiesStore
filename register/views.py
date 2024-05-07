from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.template import loader
from rest_framework.response import Response
import bcrypt
from login.models import Accounts
import uuid


# Create your views here.
def register(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render())

@api_view(['POST'])
def handler_register(request):
    data = request.data
    try:
        Accounts.objects.get(email=data['email'])
        return Response({
           'message': 'Email already exists'
        })
    except Accounts.DoesNotExist:
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt(12))
        account = Accounts(id=uuid.uuid1(), email=data['email'], user_name=data['name'], password=hashed_password.decode('utf-8'), role='user', is_verified=False)
        account.save()
        return Response({
            'message': 'Register account is successfully'
        })
