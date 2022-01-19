from django import template
register = template.Library()


@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for slug in keys:
        if str(slug) == product.slug:
            return cart.get(slug)
    return 0


@register.filter(name='total_price')
def total_price(product, cart):
    return product.price * cart_quantity(product, cart)


@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    total = 0
    for product in products:
        total += total_price(product, cart)
    return total


@register.filter(name='quantity_total')
def number_of_products(products, cart):
    quantity_total = 0
    for product in products:
        quantity_total += cart_quantity(product, cart)
    return quantity_total


@register.filter(name='order_total_price')
def order_total_price(price, quantity):
    return price * quantity
