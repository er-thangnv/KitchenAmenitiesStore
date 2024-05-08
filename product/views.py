from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products
from .serializers import ProductsSerializer

# Create your views here.
@api_view(['GET'])
def get_new_products(request):
    new_products = Products.objects.order_by('-created_at')[:10]
    serializer = ProductsSerializer(new_products, many=True)
    return Response({
        'message': 'Success',
        'data': serializer.data 
    }) 
