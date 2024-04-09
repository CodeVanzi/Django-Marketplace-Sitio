from django.conf import settings
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from product.models import Product
from order.models import Order
from .cart import Cart
from django.http import HttpResponse

from django.http import JsonResponse
from core.utils.correios import validar_cep
import requests



# def update_menu_cart(request, product_id, action):
#     cart = Cart(request)
#     product = Product.objects.get(id=product_id)
    
#     if action == 'increment':
#         cart.add(product=product, quantity=1, update_quantity=True)
#     elif action == 'decrement':
#         cart.add(product=product, quantity=-1, update_quantity=True)
#     elif action == 'remove':
#         cart.remove(product=product, update_quantity=True)
#     elif action == 'clear':
#         cart.clear()
    
#     response = render(request, 'cart/partials/menu_cart.html', {'cart': cart})
#     response['HX-Trigger'] = 'update-menu-cart'
    
#     return response


def update_cart(request, product_id, action):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    
  
    if action == 'increment':
        cart.add(product=product, quantity=1, update_quantity=True)
    elif action == 'decrement':
        cart.add(product=product, quantity=-1, update_quantity=True)
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
                'slug': product.slug,
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

def remove_all_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove_all(product_id)
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
    payment_options = Order.PAYMENT_CHOICES
    hora_entrega = Order.HORA_CHOICES
    
    context = {
        'pub_key': pub_key,
        'payment_options': payment_options,
        'hora_entrega': hora_entrega,
    }
    return render(request, 'cart/checkout.html', context)



def validar_cep(request, zipcode):
    cep = zipcode.replace('-', '')
    url = f'https://viacep.com.br/ws/{cep}/json/'

    try:
        response = requests.get(url)
        data = response.json()
        if not data.get('erro'):
            return JsonResponse({'valido': True, 'endereco': data})
        else:
            return JsonResponse({'valido': False, 'mensagem': 'CEP invalido'})
    except Exception as e:
        return JsonResponse({'valido': False, 'mensagem': 'Erro ao consultar o CEP'})

def hx_menu_cart(request):
    cart = Cart(request)
    return render(request, 'cart/partials/menu_cart.html', {'cart': cart})

def hx_cart_total(request):
    cart = Cart(request)
    return render(request, 'cart/partials/cart_total.html', {'cart': cart})


def success(request):
    return render(request, 'cart/success.html')