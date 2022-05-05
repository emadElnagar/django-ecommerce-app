from itertools import product
from django.shortcuts import render, redirect
from django.urls import reverse
from shop.models import Product
from django.contrib import messages
from .models import Order
from django.contrib.auth.decorators import login_required


def add_to_cart(request, slug):
    product = Product.objects.get(slug=slug)
    cart = request.session.get('cart')
    sucees_message = "product added successfully to cart"
    if cart:
        quantity = cart.get(product.slug)
        if quantity:
            cart[product.slug] += 1
            messages.success(request, sucees_message)
        else:
            cart[product.slug] = 1
            messages.success(request, sucees_message)
    else:
        cart = {}
        cart[product.slug] = 1
        messages.success(request, sucees_message)
    request.session['cart'] = cart
    return redirect(reverse('shop:product_detail', kwargs={'slug':product.slug}))


def cart_details(request):
    products = None
    if request.session.get('cart'):
        slugs = list(request.session.get('cart').keys())
        products = Product.get_products_by_slug(slugs)
    return render(request, 'cart/cart_details.html', {'products':products})


def quantity_plus(request, slug):
    product_slug = request.POST.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product.slug)
        if quantity:
            cart[product.slug] += 1
    request.session['cart'] = cart
    return redirect(reverse('cart:cart_details'))


def quantity_minus(request, slug):
    product_slug = request.POST.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product.slug)
        if quantity > 1:
            cart[product.slug] -= 1
        else:
            del cart[product.slug]
    request.session['cart'] = cart
    return redirect(reverse('cart:cart_details'))


def remove_from_cart(request, slug):
    product_slug = request.POST.get('product_slug')
    product = Product.objects.get(slug=product_slug)
    cart = request.session.get('cart')
    if cart:
        del cart[product.slug]
    request.session['cart'] = cart
    return redirect(reverse('cart:cart_details'))


def clear_cart(request):
    cart = request.session.get('cart')
    if cart:
        cart.clear()
    request.session['cart'] = cart
    return redirect(reverse('cart:cart_details'))


@login_required
def place_order(request):
    cart = request.session.get('cart')
    if cart:
        return render(request, 'cart/place_order.html', {})
    else:
        return redirect('shop:product_list')


@login_required
def checkout(request):
    if request.method == 'POST':
        country = request.POST.get('country')
        city = request.POST.get('city')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        phoneTwo = request.POST.get('phoneTwo')
        customer = request.user
        cart = request.session.get('cart')
        products = Product.get_products_by_slug(list(cart.keys()))

        for product in products:
            order = Order(
                country = country,
                city = city,
                address = address,
                phone = phone,
                phoneTwo = phoneTwo,
                customer = customer,
                price = product.price,
                product = product,
                quantity = cart.get(str(product.slug))
            )
            order.placeOrder()
        request.session['cart'] = {}
    return redirect('shop:product_list')


@login_required
def OrderHistory(request):
    customer = request.user
    orders = Order.get_orders_by_customer(customer)
    return render(request, 'cart/order-history.html', {'orders': orders})
