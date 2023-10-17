from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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

def cart(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')