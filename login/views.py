from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.template import loader
import bcrypt
from django.http import HttpResponse
from login.models import Accounts

# Create your views here.
def login(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

@api_view(['POST'])
def handler_login(request):
  data = request.data
  try:
      account = Accounts.objects.get(email=data['email'])
      if account.is_verified == False:
         return Response({
          'message': 'Account is not verification'
        })
      password_hashed = account.password.encode('utf-8')
      password = data['password']
      password_bytes = password.encode('utf-8')
      result = bcrypt.checkpw(password_bytes, password_hashed) 
      if result:
        request.session["current_user_id"] = str(account.id)
        return Response({
        'message': 'Login is successfully'
        }) 
      else:
        return Response({
          'message': 'Login is failed'
        })
  except Accounts.DoesNotExist:
      return Response({
        'message': 'Login is failed'
      })