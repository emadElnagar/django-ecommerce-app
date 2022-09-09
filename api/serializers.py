from rest_framework import serializers
from shop.models import Category, Product, Review
from accounts.models import Profile
from cart.models import Order
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        # fields = '__all__'
        exclude = ('expire','customer')
