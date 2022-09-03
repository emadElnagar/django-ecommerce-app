from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Category, Product, Review
from .forms import ReviewForm


#### CATEGORY VIEWS
class CategoryList(ListView):
    model = Category
    ordering = ['-id']


def CategoryDetail(request, slug):
    try:
        category = Category.objects.get(slug=slug)
    except Category.DoesNotExist:
        raise Http404
    product = Product.objects.filter(category=category)
    return render(request, 'shop/category_detail.html', {'category':category, 'products':product})


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'image']

    def get_success_url(self):
        return reverse('shop:category_list')


class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'image']

    def get_success_url(self):
        return reverse('shop:category_list')


class CategoryDelet(DeleteView):
    model = Category

    def get_success_url(self):
        return reverse('shop:category_list')


#### PRODUCT VIEWS
class ProductList(ListView):
    model = Product
    ordering = '-last_update'
    paginate_by = 9
    def get_context_data(self, **kwargs):
        context = super(ProductList, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


def Search(request):
    product = None
    # SEARCH RESUTL
    if 'search' in request.GET:
        name = request.GET['search']
        if name:
            product = Product.objects.filter(name__icontains=name)
    return render(request, 'shop/search.html', {'products':product,'name':name})


def ProductDetail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        raise Http404
    related_products = Product.objects.filter(category=product.category).order_by('-last_update').exclude(id=product.id)[:3]
    other_products = Product.objects.filter(owner=product.owner).order_by('-last_update').exclude(id=product.id)[:3]
    reviews = Review.objects.filter(product=product.id).order_by('-created_at')
    reviews_count = reviews.count()
    reviews_avg = reviews.aggregate(Avg("rate"))["rate__avg"]
    if reviews_avg != None:
        reviews_avg = round(reviews.aggregate(Avg("rate"))["rate__avg"], 1)

    # REVIEW FORM
    if request.method == 'POST':
        review_form = ReviewForm(request.POST or None)
        if review_form.is_valid():
            content = request.POST.get('comment')
            rate = request.POST.get('rate')
            review = Review.objects.create(product = product, user = request.user, rate=rate ,comment = content)
            review.save()
            return HttpResponseRedirect(product.get_absolute_url())
    else:
        review_form = ReviewForm()

    context = {
        'product':product,
        'related_products':related_products,
        'other_products':other_products,
        'reviews':reviews,
        'review_form':review_form,
        'reviews_count':reviews_count,
        'reviews_avg':reviews_avg
    }
    return render(request, 'shop/product_detail.html', context)


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'description', 'image', 'price', 'discount', 'in_stock', 'category', 'is_valid']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('shop:product_list')


class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'description', 'image', 'price', 'discount', 'in_stock', 'category', 'is_valid']
    template_name = 'shop/product_update.html'

    def get_success_url(self):
        return reverse('shop:product_list')


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product

    def get_success_url(self):
        return reverse('shop:product_list')


@login_required
def wishlist(request, slug):
    user = request.user
    product = Product.objects.get(slug=slug)
    if request.method == 'POST':
        if user in product.wished.all():
            product.wished.remove(user)
        else:
            product.wished.add(user)
    return redirect(reverse('shop:product_detail', kwargs={"slug": product.slug}))


@login_required
def WishListView(request):
    product = Product.objects.filter(wished=request.user)
    return render(request, 'shop/wishlist.html', {'products':product})
