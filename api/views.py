from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer
from shop.models import Category, Product, Review

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
@api_view(['GET', 'PUT', 'DELETE'])
def SingleCategory(request, slug):
    category = Category.objects.get(slug = slug)
    # get all category products
    if request.method == 'GET':
        products = Product.objects.filter(category = category)
        serializer = ProductSerializer(products, many = True)
        return Response(serializer.data)
    # update category
    elif request.method == 'PUT':
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

# SINGLE PRODUCTS VIEW
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def SingleProduct(request, slug):
    product = Product.objects.get(slug = slug)
    # Get Single Product
    if request.method == 'GET':
        related_products = Product.objects.filter(category=product.category).order_by('-last_update').exclude(id=product.id)[:3]
        other_products = Product.objects.filter(owner=product.owner)
        reviews = Review.objects.filter(product = product)
        # Serializers
        productSerializer = ProductSerializer(product)
        relatedProductsSerializer = ProductSerializer(related_products, many = True)
        otherProductsSerializer = ProductSerializer(other_products, many = True)
        reviewSerializer = ReviewSerializer(reviews, many = True)
        return Response({
            'product': productSerializer.data,
            'relatedProducts': relatedProductsSerializer.data,
            'otherProducts': otherProductsSerializer.data,
            'reviews': reviewSerializer.data
        })
    # Update Single Product
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    # Delete Product
    elif request.method == 'DELETE':
        if product:
            product.delete()
            return Response({"status":"ok"}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    # Create Review
    elif request.method == 'POST':
        serializer = ReviewSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# CREATE NEW PRODUCT
@api_view(['POST'])
def NewProduct(request):
    if request.method == 'POST':
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# SEARCH API
@api_view(['GET'])
def Search(request):
    product = None
    if 'search' in request.GET:
        name = request.GET['search']
        if name:
            products = Product.objects.filter(name__icontains=name)
            serializer = ProductSerializer(products, many = True)
            return Response(serializer.data)

# UPDATE REVIEW
@api_view(['PUT'])
def UpdateReview(request, pk):
    review = Review.objects.filter(id = pk)
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# DELETE REVEIW
@api_view(['DELETE'])
def DeleteReview(request, pk):
    review = Review.objects.filter(id = pk)
    if request.method == 'DELETE':
        if review:
            review.delete()
            return Response({"status":"ok"}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
