from rest_framework import serializers
from shop.models import Category, Product, Review
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

class ChangePasswordSerializer(serializers.Serializer):
    class Meta:
        model = User
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True)
