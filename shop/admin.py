from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Category, Product, Review


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.unregister(Group)
