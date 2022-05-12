from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.dispatch import receiver
from django.urls import reverse
from ckeditor.fields import RichTextField
import os



class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category/')
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Category)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ DELETE CATEGORY IMAGE AUTOMATICALLY FROM MEDIA AFTER DELETEING CATEGORY """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Category)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """ DELETE CATEGORY IMAGE AUTOMATICALLY FROM MEDIA AFTER UPDATING CATEGORY """
    if not instance.pk:
        return False
    try:
        old_file = Category.objects.get(pk=instance.pk).image
    except Category.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField()
    image = models.ImageField(upload_to='products/')
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    in_stock = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, related_name='product_category',null=True, blank=True)
    is_valid = models.BooleanField(default=True)
    is_BestSeller = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    wished = models.ManyToManyField(User, related_name='favourite')
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product,self).save(*args, **kwargs)

    def get_price(self):
        if self.discount != None:
            return self.price - self.discount
        else:
            return self.price

    def get_discount_percent(self):
        discount_percent = round((self.discount/self.price) * 100)
        return f"{discount_percent}% off"

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug':self.slug})

    @staticmethod
    def get_products_by_slug(slugs):
        return Product.objects.filter(slug__in = slugs)

    def __str__(self):
        return self.name


@receiver(models.signals.post_delete, sender=Product)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """ DELETE PRODUCT IMAGE AUTOMATICALLY FROM MEDIA AFTER DELETEING PRODUCT """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Product)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """ DELETE PRODUCT IMAGE AUTOMATICALLY FROM MEDIA AFTER UPDATING PRODUCT """
    if not instance.pk:
        return False
    try:
        old_file = Product.objects.get(pk=instance.pk).image
    except Product.DoesNotExist:
        return False
    new_file = instance.image
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(f"{self.user} liked {self.product}")


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField()
    rate = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} review on {self.product}"
