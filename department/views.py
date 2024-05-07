from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from department.models import Departments
from .serializers import DepartmentsSerializer 

# Create your views here.
@api_view(['GET'])
def get_departments(request):
    departments = Departments.objects.all()
    serializer = DepartmentsSerializer(departments, many=True) 
    return Response({
        'message': 'Success',
        'data': serializer.data 
    })
