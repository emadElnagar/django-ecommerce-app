from unicodedata import category
from django.shortcuts import render
from shop.models import Product, Category

# Create your views here.
def home(request):
    products = Product.objects.all().order_by('-last_update')[:6]
    categories = Category.objects.all().order_by('-pk')[:4]
    context = {
        "products": products,
        "categories": categories,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    return render(request, 'pages/about.html', {})

def error_404_view(request, exception):
    return render(request, 'pages/not_found.html')

def error_500_view(request, *args, **kwargs):
    return render(request, 'pages/server_internal_error.html')
