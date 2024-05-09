import os
from dotenv import load_dotenv
from rest_framework.decorators import api_view
import base64
import requests
import json
from rest_framework.response import Response
from order.models import Orders, OrderDetails, Status, Payments
from django.http import QueryDict

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
    print(isinstance(data, QueryDict))
    if isinstance(data, QueryDict):
        data_json = json.loads(list(data.keys())[0])
        customer_info = data_json['customer_info']
        order_info = data_json['order_info']
        if data_json['payment_method'] == 'cod':
            order = Orders(customer_name=customer_info['customer_name'], address=customer_info['address'], phone_number=customer_info['phone_number'], email=customer_info['email'], note=customer_info['note'], sub_total=order_info['total_price'], amount=1, total=order_info['total_price'], status=Status.WAITING.value, payment_method_id=1, account_id=account_id)
            order.save()
            order_details = OrderDetails(product_id=order_info['product_id'], order_id=order.id)
            order_details.save()
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
