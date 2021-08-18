from rest_framework import status
from rest_framework.decorators import api_view
from products.models import Product
from .serialixers import ProductSerializer
from rest_framework.response import Response


@api_view(["GET"])
def product_all(request):
    products = Product.objects.all()
    data = ProductSerializer(products, many=True).data
    return Response(data=data)


@api_view(["GET"])
def product_object(request, id):
    products = Product.objects.get(id=id)
    data = ProductSerializer(products, many=False).data
    return Response(data=data)
