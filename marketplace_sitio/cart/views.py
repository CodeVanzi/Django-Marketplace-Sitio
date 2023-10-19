from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from product.models import Product


# Create your views here.
from .cart import Cart

def update_cart(request, product_id, action):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    
    if action == 'increment':
        cart.add(product=product, quantity=1, update_quantity=True)
    elif action == 'decrement':
        cart.add(product=product, quantity=-1, update_quantity=True)
    elif action == 'remove':
        cart.remove(product=product)
    elif action == 'clear':
        cart.clear()
    
    return render(request, 'cart/partials/menu_cart.html', {'cart': cart})

# def update_cart(request, product_id, action):
#     cart = Cart(request)
#     product = Product.objects.get(id=product_id)
#     cart.add(product=product, quantity=1, update_quantity=True)
#     # cart.remove(product=product)
#     # cart.clear()
#     return render(request, 'cart/partials/menu_cart.html', {'cart': cart})

def cart(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')

def hx_menu_cart(request):
    return render(request, 'cart/partials/menu_cart.html')