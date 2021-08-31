from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.admin import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from products.models import Product, Category, Review, Tag
from .serialixers import ProductSerializer, ReviewSerializer
from rest_framework.response import Response
from .serialixers import CategoryWithProductSerializer, ReviewWithProductSerializer, ProductCreateSerializer


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


@api_view(["GET"])
def category_product_list(request):
    categories = Category.objects.all()
    category = categories[2]
    print(category.products.all())
    data = CategoryWithProductSerializer(categories, many=True).data
    return Response(data=data)


@api_view(["GET"])
def reviews(request):
    review = Review.objects.all()
    print(review.products.all())
    data = ReviewWithProductSerializer(review, many=True).data
    return Response(data=data)


@api_view(['POST'])
def tags_views(request):
    name = request.data['name']
    Tag.objects.create(name=name)
    return Response(data={"message": 'OK'})


@api_view(['PUT', 'DELETE'])
def tags_update_delete_views(request, id):
    try:
        tag = Tag.objects.get(id=id)
    except Tag.DoesNotExist:
        return Response(data={'message': 'Tag not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == "DELETE":
        tag.delete()
        return Response(data={'message': 'tag deleted!'})

    elif request.method == "PUT":
        name = request.data['name']
        tag.name = name
        tag.save()
        return Response(data={'message': 'Tag updated!'})


@api_view(['PUT', 'DELETE'])
def product_put_delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == "DELETE":
        product.delete()
        return Response(data={'message': 'product deleted!'})
    if request.method == 'PUT':
        serializer = ProductCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={
                'message': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_406_NOT_ACCEPTABLE)
        product = Product.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            price=request.data['price'],
            category_id=request.data['category_id'],
        )
        for i in request.data['tags']:
            product.tags.add(i)
        product.save()
        return Response(data={'message': 'Ok'})


@api_view(['POST', "GET"])
@permission_classes([IsAuthenticated])
def reviews_views(request):
    if request.method == 'POST':
        Review.objects.create(
            text=request.data['text'],
            product_id=request.data['product_id'],
            author=request.user
        )
        return Response(data={'message': 'OK'})
    elif request.method == 'GET':
        reviews = Review.objects.filter(author=request.user)
        return Response(data=ReviewSerializer(reviews, many=True).data)


@api_view(['POST'])
def login(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username,password=password)
    if user is None:
        return Response(data={'message': 'User not found or Wrong password'},
                        status=status.HTTP_404_NOT_FOUND)
    if user:
        try:
            token = Token.objects.get(user=user)
        except:
            token = Token.objects.create(user=user)
        return Response(data={'key': token.key})
