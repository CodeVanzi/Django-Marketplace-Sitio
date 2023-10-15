from django.shortcuts import render

from product.models import Product


# Create your views here.
from .cart import Cart

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product, quantity=1, update_quantity=True)
    # cart.remove(product=product)
    # cart.clear()
    return render(request, 'cart/menu_cart.html', {'cart': cart})