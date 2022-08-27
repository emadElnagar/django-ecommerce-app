from django.urls import path
from . import views

app_name ='shop'

urlpatterns = [
    # CATEGORY API
    path('category/all', views.GetAllCategories),
    path('category/new', views.NewCategory),
    path('category/<str:slug>', views.SingleCategory),
    # PRODUCTS API
    path('products/all', views.ProductsList),
    path('products/new', views.NewProduct),
    path('products/<str:slug>', views.SingleProduct),
    # SEARCH API
    path('Search', views.Search),
]
