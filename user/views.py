from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from login.models import Accounts

# Create your views here.
@api_view(['GET'])
def get_user_current(request):
    current_user_id = request.session.get("current_user_id")
    account = Accounts.objects.get(id=current_user_id)
    return Response({
        'message': 'Success',
        'data': {
            'current_user_id': current_user_id,
            'name': str(account.user_name),
            'email': str(account.email),
            'role': str(account.role)
        }
    }) 

@api_view(['GET'])
def log_out(request):
    try:
        del request.session["current_user_id"]
    except KeyError:
        pass
    return Response({
        'message': 'Success'
    }) 
