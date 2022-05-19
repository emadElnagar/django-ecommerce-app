from itertools import product
from django.db import models
from django.contrib.auth.models import User
from shop.models import Product
from phonenumber_field.modelfields import PhoneNumberField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = PhoneNumberField(null=False, blank=False)
    phoneTwo = PhoneNumberField(null=True, blank=True)
    card_number = CardNumberField(null=True, blank=True)
    expire = CardExpiryField(null=True, blank=True)
    security_code = SecurityCodeField(null=True, blank=True)

    def __str__(self):
        return f"order {self.pk}"
    
    def placeOrder(self):
        self.save()
    
    @staticmethod
    def get_orders_by_customer(customer):
        return Order.objects.filter(customer = customer)
