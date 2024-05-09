from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Products, DescriptionsProduct
from .serializers import ProductsSerializer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@api_view(['GET'])
def get_new_products(request):
    new_products = Products.objects.order_by('-created_at')[:10]
    serializer = ProductsSerializer(new_products, many=True)
    return Response({
        'message': 'Success',
        'data': serializer.data 
    }) 

@api_view(['GET'])
def get_details_product(request, id):
    product = Products.objects.get(id=id)
    description = DescriptionsProduct.objects.get(product_id=id)
    details_product = {
        'id': id,
        'name': product.name,
        'price': product.price,
        'images': [
            description.image1,
            description.image2,
            description.image3,
            description.image4,
        ],
        'description': description.description,
        'video': description.video_url,
        'brand': description.brand,
        'color': description.color,
        'status': description.status
    }
    context = {
        'details_product': details_product
    }
    return render(request, 'details-product.html', context)

@api_view(['GET'])
def get_all_products(request):
    products_list = Products.objects.all()
    paginator = Paginator(products_list, 8)
    page_number = request.GET.get("page")
    try:
        products = paginator.page(int(page_number))
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    serializer = ProductsSerializer(products, many=True)
    has_next_page = products.has_next()
    return Response({
        'message': 'Success',
        'data': {
            'items': serializer.data,
            'page': page_number,
            'has_next_page': has_next_page
        }
    }) 