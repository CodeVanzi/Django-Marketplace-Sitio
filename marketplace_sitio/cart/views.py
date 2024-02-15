from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from product.models import Product
from .cart import Cart




def update_menu_cart(request, product_id, action):
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
    
    response = render(request, 'cart/partials/menu_cart.html', {'cart': cart})
    response['HX-Trigger'] = 'update-menu-cart'
    
    return response


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
    
    quantity = cart.get_item(product_id)
            
    if quantity:
        quantity = quantity['quantity']
        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
                'description': product.description,
            },
            'total_price': quantity * product.price,
            'quantity': quantity,
        }
    else:
        item = None
    
    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'
    
    return response


def cart(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

@login_required
def checkout(request):
    pub_key = settings.STRIPE_API_KEY_PUBLISHABLE
    return render(request, 'cart/checkout.html', {'pub_key': pub_key})

def hx_menu_cart(request):
    cart = Cart(request)
    return render(request, 'cart/partials/menu_cart.html', {'cart': cart})

def hx_cart_total(request):
    cart = Cart(request)
    return render(request, 'cart/partials/cart_total.html', {'cart': cart})