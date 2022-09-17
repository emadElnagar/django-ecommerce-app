from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer, ChangePasswordSerializer, UserProfileSerializer, UserSerializer, OrderSerializer
from shop.models import Category, Product, Review
from accounts.models import Profile
from cart.models import Order
from django.contrib.auth.models import User

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
    try:
        category = Category.objects.get(slug = slug)
    except Category.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
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
    try:
        product = Product.objects.get(slug = slug)
    except Product.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    # Get Single Product
    if request.method == 'GET':
        related_products = Product.objects.filter(category=product.category).order_by('-last_update').exclude(id=product.id)[:3]
        other_products = Product.objects.filter(owner=product.owner).order_by('-last_update').exclude(id=product.id)[:3]
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
    try:
        review = Review.objects.filter(id = pk)
    except Review.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        serializer = ReviewSerializer(review, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# DELETE REVEIW
@api_view(['DELETE'])
def DeleteReview(request, pk):
    try:
        review = Review.objects.filter(id = pk)
    except Review.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        if review:
            review.delete()
            return Response({"status":"ok"}, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

#========== AUTH API ==========#

# USER PROFILE VIEW
class UserProfile(APIView):
    # Get profile data
    def get(self, request, pk):
        try:
            profile = Profile.objects.get(id = pk)
        except Profile.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile, many = False)
        return Response(serializer.data)
    # update user profile data
    def put(self, request, pk):
        try:
            profile = Profile.objects.get(id = pk)
        except Profile.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

# USER DATA VIEW
class UserView(APIView):
    # Get user data
    def get(self, request, pk):
        try:
            user = User.objects.get(id = pk)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, many = False)
        return Response(serializer.data)
    # Update user data
    def put(self, request, pk):
        try:
            user = User.objects.get(id = pk)
        except User.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# SIGN UP
@api_view(['POST'])
def SignUp(request):
    if request.method == 'POST':
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST) 

# DELETE ACCOUNT
@api_view(['DELETE'])
def DeleteUser(request):
    user = request.user
    if user.is_authenticated:
        user.delete()
        return Response({"status":"ok"}, status = status.HTTP_200_OK)
    return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# CHANGE PASSWORD VIEW
class ChangePasswordView(APIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj
    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#========== ORDER API ==========#

# Order
class OrderView(APIView):
    # Get user orders
    def get(self, request):
        customer = request.user
        if customer.is_authenticated:
            orders = Order.objects.filter(customer = customer)
            serializer = OrderSerializer(orders, many = True)
            return Response(serializer.data)
        return Response(status = status.HTTP_403_FORBIDDEN)
    # New order
    def post(self, request):
        customer = request.user
        if customer.is_authenticated:
            serializer = OrderSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_403_FORBIDDEN)

# SINGLE ORDER
class SingleOrder(APIView):
    # Get single order
    def get(self, request, pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated and request.user.id == order.customer.id:
            serializer = OrderSerializer(order, many = False)
            return Response(serializer.data)
        return Response(status = status.HTTP_403_FORBIDDEN)
    # Delete order
    def delete(self, request, pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated and request.user.id == order.customer.id:
            if order:
                order.delete()
                return Response({"status":"ok"}, status = status.HTTP_200_OK)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)
    # Update order
    def put(self, request, pk):
        try:
            order = Order.objects.get(id = pk)
        except Order.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        if request.user.is_authenticated and request.user.id == order.customer.id:
            serializer = OrderSerializer(order, data = request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
        return Response(status = HTTP_405_METHOD_NOT_ALLOWED)
