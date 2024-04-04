from django.conf import settings
from django.shortcuts import render
from datetime import datetime
from cart.cart import Cart
from .models import Order, OrderItem
import json
import stripe
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def start_order(request):
    cart = Cart(request)
    data = json.loads(request.body)
    total_price = 0

    items = []

    for item in cart:
        product = item['product']
        total_price += product.price * int(item['quantity'])
        
        obj = {
            'price_data': {
                'currency': 'brl',
                'product_data': {
                    'name': product.name,
                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': int(item['quantity']),
        }
        
        items.append(obj)
   
    payment_method = 'boleto' if data['forma_pagamento'] == 'Boleto' else 'card'
    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN
    session = stripe.checkout.Session.create(
        payment_method_types=[payment_method],
        line_items=items,
        mode='payment',
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )
    payment_intent = session.payment_intent        

    first_name = data['first_name']
    last_name = data['last_name']
    email = data['email']
    address = data['address']
    zipcode = data['zipcode']
    cidade = data['cidade']
    phone = data['phone']
    hora_entrega = data['hora_entrega']    
    # Convertendo a data de entrega para o formato correto
    data_entrega = datetime.strptime(data['data_entrega'], '%d/%m/%Y').strftime('%Y-%m-%d')    
    vendedor_nome = data['vendedor_nome']
    telefone_vendedor = data['telefone_vendedor']
    vendedor_email = data['vendedor_email']
    forma_pagamento = data['forma_pagamento']

    order = Order.objects.create(
        user=request.user,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        address=address,
        zipcode=zipcode,
        cidade=cidade,
        hora_entrega=hora_entrega,
        data_entrega=data_entrega,
        vendedor_nome=vendedor_nome,
        telefone_vendedor=telefone_vendedor,
        vendedor_email=vendedor_email,
        forma_pagamento=forma_pagamento,
        payment_intent=payment_intent,
        paid = True if payment_intent else False,
        paid_amount = total_price
    )
    order.save()

    for item in cart:
        product = item['product']
        quantity = int(item['quantity'])
        price = product.price * quantity

        item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
        
    cart.clear()

    return JsonResponse({'session': session, 'order': payment_intent})

@login_required
def myorders(request):
    return render(request, 'order/myorders.html')
