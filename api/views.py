from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer
from shop.models import Category, Product

# GET ALL CATEGORIES
@api_view(['GET'])
def GetAllCategories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many = True)
    return Response(serializer.data)

# CREATE NEW CATEGORY
@api_view(['POST'])
def NewCategory(request):
    serializer = CategorySerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# SINGLE CATEGORY VIEW
@api_view(['PUT', 'DELETE'])
def SingleCategory(request, slug):
    category = Category.objects.get(slug = slug)
    # update category
    if request.method == 'PUT':
        serializer = CategorySerializer(category, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    # delete category
    elif request.method == 'DELETE':
        if category:
            category.delete()
            return Response({"status":"ok"}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# PRODUCTS LIST VIEW
@api_view(['GET'])
def ProductsList(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many = True)
    return Response(serializer.data)
