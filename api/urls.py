from django.urls import path
from . import views

app_name ='shop'

urlpatterns = [
    # CATEGORY API
    path('category/all', views.GetAllCategories),
    path('category/new', views.NewCategory),
    path('category/<str:slug>', views.SingleCategory),
    path('products/all', views.ProductsList),
]
