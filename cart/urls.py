from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('add_to_cart/<str:slug>', views.add_to_cart, name='add_to_cart'),
    path('cart-details', views.cart_details, name='cart_details'),
    path('quantity-plus/<str:slug>', views.quantity_plus, name='quantity_plus'),
    path('quantity-minus/<str:slug>', views.quantity_minus, name='quantity_minus'),
    path('remove-from-cart/<str:slug>', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
]