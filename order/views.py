import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view
import base64
from django.shortcuts import render
import requests
import json
from rest_framework.response import Response
from order.models import Orders, OrderDetails, Status, Payments, PaymentMethods
from product.models import Products, DescriptionsProduct
from django.http import QueryDict
from .serializers import OrdersSerializer
from datetime import datetime
from login.models import Accounts
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django_rq import job

load_dotenv()

# Create your views here.
@api_view(['POST'])
def create_order(request):
    data = request.data
    current_user_id = request.session.get("current_user_id")
    if current_user_id is None:
        account_id = ''
    else:
        account_id = current_user_id
    if isinstance(data, QueryDict):
        data = request.data
        data_json = {}
        for key, value in data.items():
            data_json[key] = value
        customer_info = {}
        for key, value in data_json.items():
            if key.startswith('customer_info['):
                field_name = key.split('[')[1].split(']')[0]
                customer_info[field_name] = value
        order_info = {}
        for key, value in data_json.items():
            if key.startswith('order_info['):
                field_name = key.split('[')[1].split(']')[0]
                order_info[field_name] = value
        if data_json['payment_method'] == 'cod':
            order = Orders(customer_name=customer_info['customer_name'], address=customer_info['address'], phone_number=customer_info['phone_number'], email=customer_info['email'], note=customer_info['note'], sub_total=order_info['total_price'], amount=1, total=order_info['total_price'], status=Status.WAITING.value, payment_method_id=1, account_id=account_id)
            order.save()
            order_details = OrderDetails(product_id=order_info['product_id'], order_id=order.id)
            order_details.save()
            context = get_data_details_order(current_user_id, order.id)
            send_invoice_to_email.delay(context, customer_info['email'])
            return Response({
                'message': 'Success',
                'data': {
                    "payment_method_name": "cod",
                    "order_id": order.id,
                    "payment_order_id": None
                }
        })
    else:
        customer_info = data['customer_info']
        order_info = data['order_info']
        access_token = generateAccessToken()
        paypal_url_base = os.getenv('PAYPAL_URL_BASE')
        url = f"{paypal_url_base}/v2/checkout/orders"

        order = Orders(customer_name=customer_info['customer_name'], address=customer_info['address'], phone_number=customer_info['phone_number'], email=customer_info['email'], note=customer_info['note'], sub_total=order_info['total_price'], amount=1, total=order_info['total_price'], status=Status.WAITING.value, payment_method_id=2, account_id=account_id)
        order.save()
        order_details = OrderDetails(product_id=order_info['product_id'], order_id=order.id)
        order_details.save()

        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": round(order_info['total_price'] * 0.00003931, 1)
                    }
                }
            ]
        }

        try:
            response = requests.post(
                url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {access_token}"
                },
                data=json.dumps(payload)
            )
            response_json = response.json()
            payment = Payments(order_id=order.id, payment_order_id=response_json['id'])
            payment.save()
            return Response({
                'message': 'Success',
                'data': {
                    "payment_method_name": "paypal",
                    "order_id": order.id,
                    "payment_order_id": response_json['id']
                }
            })
        except Exception as e:
            raise requests.RequestException("Payment paypal is failed")

@api_view(['POST'])
def capture_order(request, payment_order_id):
    current_user_id = request.session.get("current_user_id")
    user = Accounts.objects.get(id=current_user_id)
    access_token = generateAccessToken()
    paypal_url_base = os.getenv('PAYPAL_URL_BASE')
    url = f"{paypal_url_base}/v2/checkout/orders/{payment_order_id}/capture"

    try:
        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {access_token}"
            }
        )
        json_response = response.json()

        if json_response["status"] == "COMPLETED":
            payment = Payments.objects.get(payment_order_id=payment_order_id)
            order = Orders.objects.get(id=payment.order_id)
            order.status = Status.SUCCESS.value
            order.save()
            context = get_data_details_order(current_user_id, order.id)
            send_invoice_to_email.delay(context, user.email)
            return Response({
                'message': 'Success',
                'data': {
                    "payment_method_name": "paypal",
                    "order_id": payment.order_id,
                    "payment_order_id": payment_order_id
                }
            })
    except Exception as e:
        raise requests.RequestException("Payment paypal is failed")

def generateAccessToken():
    paypal_client_id = os.getenv('PAYPAL_CLIENT_ID')
    paypal_client_secret = os.getenv('PAYPAL_CLIENT_SECRET')
    paypal_url_base = os.getenv('PAYPAL_URL_BASE')
    auth = base64.b64encode(f"{paypal_client_id}:{paypal_client_secret}".encode()).decode('utf-8')
    try:
        response = requests.post(
            f"{paypal_url_base}/v1/oauth2/token",
            data='grant_type=client_credentials',
            headers={
                'Authorization': f'Basic {auth}',
            }
        )
        data = response.json()
        return data.get('access_token')
    except Exception as e:
        raise requests.RequestException('Generate access token failed')
    
@api_view(['GET'])
def get_all_orders(request):
    current_user_id = request.session.get("current_user_id")
    if current_user_id is None:
        return render(request, 'login.html')
    else:
        items = []
        orders = Orders.objects.filter(account_id=current_user_id).order_by('-created_at')
        data_orders = OrdersSerializer(orders, many=True)
        for order in data_orders.data:
            payment_method = PaymentMethods.objects.get(id=order['payment_method_id'])
            order_detail = OrderDetails.objects.get(order_id=order['id'])
            product = Products.objects.get(id=order_detail.product_id)  
            timestamp = datetime.strptime(order['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
            formatted_date = timestamp.strftime("%Y %B %d")
            context = {
            'order_info': {
                'id': order['id'],
                'total_price': order['total'],
                'status': order['status'],
                'payment_method': payment_method.name, 
                'created_at': formatted_date
            },
            'product_info': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'price': product.price
            }
            } 
            items.append(context)
        account = Accounts.objects.get(id=current_user_id)
        data = {
            'items': items
        }
        data['account'] = account
        return render(request, 'order.html', data)
    
@api_view(['POST'])
def cancel_order(request, payment_order_id):
    current_user_id = request.session.get("current_user_id")
    user = Accounts.objects.get(id=current_user_id)
    payment = Payments.objects.get(payment_order_id=payment_order_id)
    order = Orders.objects.get(id=payment.order_id)
    order.status = Status.CANCEL.value
    order.save()
    context = get_data_details_order(current_user_id, order.id)
    send_invoice_to_email.delay(context, user.email)
    return Response({
        'message': 'Success',
        'data': {
            'order_id': payment.order_id
        }
    })

@api_view(['GET'])
def details_order(request, order_id):
    current_user_id = request.session.get("current_user_id")
    order = Orders.objects.get(id=order_id)
    payment_method = PaymentMethods.objects.get(id=order.payment_method_id)
    order_detail = OrderDetails.objects.get(order_id=order.id)
    product = Products.objects.get(id=order_detail.product_id)  
    description_product = DescriptionsProduct.objects.get(product_id=product.id)
    formatted_date = order.created_at.strftime("%Y %B %d")
    context = {
            'customer_info': {
                'id': current_user_id,
                'name': order.customer_name,
                'address': order.address,
                'phone_number': order.phone_number,
                'email': order.email
            },
            'order_info': {
                'id': order.id,
                'total_price': order.total,
                'status': order.status,
                'payment_method': payment_method.name, 
                'note': order.note,
                'created_at': formatted_date
            },
            'product_info': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'price': product.price,
                'brand': description_product.brand,
                'color': description_product.color,
                'description': description_product.description
            }
    } 
    account = Accounts.objects.get(id=current_user_id)
    context['account'] = account
    return render(request, 'invoice.html', context)


@job
def send_invoice_to_email(context, to_email):
    subject = f"KitchenAmenitiesStore invoice of order"
    from_email = 'KitchenAmenitiesStore@no-reply.com'
    to_emails = [to_email]
    html_content = render_to_string('send-email-invoice.html', context)
    email = EmailMultiAlternatives(subject, strip_tags(html_content), from_email, to_emails)
    email.attach_alternative(html_content, "text/html")
    email.send()

def get_data_details_order(current_user_id, order_id):
    order = Orders.objects.get(id=order_id)
    payment_method = PaymentMethods.objects.get(id=order.payment_method_id)
    order_detail = OrderDetails.objects.get(order_id=order.id)
    product = Products.objects.get(id=order_detail.product_id)  
    description_product = DescriptionsProduct.objects.get(product_id=product.id)
    formatted_date = order.created_at.strftime("%Y %B %d")
    context = {
            'customer_info': {
                'id': current_user_id,
                'name': order.customer_name,
                'address': order.address,
                'phone_number': order.phone_number,
                'email': order.email
            },
            'order_info': {
                'id': order.id,
                'total_price': order.total,
                'status': order.status,
                'payment_method': payment_method.name, 
                'note': order.note,
                'created_at': formatted_date
            },
            'product_info': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'price': product.price,
                'brand': description_product.brand,
                'color': description_product.color,
                'description': description_product.description
            }
    } 
    return context