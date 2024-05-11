from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from department.models import Departments
from .serializers import DepartmentsSerializer 
from login.models import Accounts
from product.models import Products
from product.serializers import ProductsSerializer
from trademark.models import Trademarks
from trademark.serializers import TrademarksSerializer

# Create your views here.
@api_view(['GET'])
def get_departments(request):
    departments = Departments.objects.all()
    serializer = DepartmentsSerializer(departments, many=True) 
    return Response({
        'message': 'Success',
        'data': serializer.data 
    })

@api_view(['GET'])
def get_products_by_department(request, department_id):
    products = Products.objects.filter(department_id=department_id)
    data_products = ProductsSerializer(products, many=True)
    trade_marks = Trademarks.objects.all()
    data_trademarks = TrademarksSerializer(trade_marks, many=True)
    current_user_id = request.session.get("current_user_id")
    context = {
        'items': data_products.data,
        'trade_marks': data_trademarks.data
    }
    if current_user_id is not None:
        account = Accounts.objects.get(id=current_user_id)
        context['account'] = account
    return render(request, 'category.html', context)
