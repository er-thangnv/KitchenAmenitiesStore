from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Trademarks
from .serializers import TrademarksSerializer

# Create your views here.
@api_view(['GET'])
def get_trademarks(request):
    trademarks = Trademarks.objects.all()
    serializer = TrademarksSerializer(trademarks, many=True) 
    return Response({
        'message': 'Success',
        'data': serializer.data 
    })
