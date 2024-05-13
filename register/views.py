from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
from django.template import loader
from rest_framework.response import Response
import bcrypt
from login.models import Accounts
import uuid
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import jwt
from django_rq import job

SECRET_KEY = '8Zz5tw0Ionm3XPZZfN0NOml3z9FMfmpgXwovR9fp6ryDIoGRM8EPHAB6iHsc0fb'


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
        account_id = uuid.uuid1()
        account = Accounts(id=account_id, email=data['email'], user_name=data['name'], password=hashed_password.decode('utf-8'), role='user', is_verified=False)
        account.save()
        token_verify = generate_token_verification(str(account_id))
        send_email.delay(token_verify, data['email'])
        return Response({
            'message': 'Register account is successfully'
        })
    
def generate_token_verification(account_id):
    payload = {
        'type': 'register',
        'sub': account_id
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@api_view(['GET'])
def vefiry_token(request):
    token_verify = request.GET.get("token")
    try:
        payload = jwt.decode(token_verify, SECRET_KEY, algorithms=['HS256'])
        account_id = payload['sub']
        user = Accounts.objects.get(id=account_id)
        if user is not None:
            user.is_verified = True
            user.save()
            context = {}
            return render(request, 'verified.html', context)
        else:
            return Response({
                'message': 'Failed'
            })
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None 

@job
def send_email(token_verify, to_email):
    subject = 'Email verification account KitchenAmenitiesStore'
    from_email = 'KitchenAmenitiesStore@no-reply.com'
    to_emails = [to_email]
    html_content = render_to_string('send-mail.html', {'token_verify': token_verify})
    email = EmailMultiAlternatives(subject, strip_tags(html_content), from_email, to_emails)
    email.attach_alternative(html_content, "text/html")
    email.send()