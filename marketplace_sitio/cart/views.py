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
    quantity = cart.get_item(product_id)
  
    if action == 'increment':
        cart.add(product=product, quantity=1, update_quantity=True)
    elif action == 'decrement':
        cart.add(product=product, quantity=-1, update_quantity=True)
    elif action == 'remove':
        cart.remove(product=product)
    elif action == 'clear':
        cart.clear()
            
    if quantity:
        quantity = quantity['quantity']
        item = {
            'product': {
                'id': product.id,
                'name': product.name,
                'image': product.image,
                'get_thumbnail': product.get_thumbnail(),
                'price': product.price,
            },
            'total_price': quantity * product.price,
            'quantity': quantity,
        }
    else:
        item = None
    
    response = render(request, 'cart/partials/cart_item.html', {'item': item})
    response['HX-Trigger'] = 'update-menu-cart'
    
    return response

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

# def cart_item(request, product_id):
#     cart = Cart(request)
#     product = Product.objects.get(pk=product_id)
#     quantity = cart.get_item(product_id)
#     if quantity:
#         quantity = quantity['quantity']

#         item = {
#             'product': {
#                 'id': product.id,
#                 'name': product.name,
#                 'image': product.image,
#                 'description': product.description,
#                 'get_thumbnail': product.get_thumbnail(),
#                 'price': product.price,
#             },
#             'total_price': quantity * product.price,
#             'quantity': quantity,
#         }
#     else:
#         item = None
    
#     return render(request, 'cart/partials/cart_item.html', {'item': item})

@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')

def hx_menu_cart(request):
    cart = Cart(request)
    return render(request, 'cart/partials/menu_cart.html', {'cart': cart})