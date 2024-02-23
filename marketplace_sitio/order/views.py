from django.shortcuts import render, redirect
from datetime import datetime
from cart.cart import Cart
from .models import Order, OrderItem

def start_order(request):
    cart = Cart(request)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        zipcode = request.POST.get('zipcode')
        cidade = request.POST.get('cidade')
        phone = request.POST.get('phone')
        hora_entrega = request.POST.get('hora_entrega')
        
        # Convertendo a data de entrega para o formato correto
        data_entrega = datetime.strptime(request.POST.get('data_entrega'), '%d/%m/%Y').strftime('%Y-%m-%d')
        
        vendedor_nome = request.POST.get('vendedor_nome')
        telefone_vendedor = request.POST.get('telefone_vendedor')
        vendedor_email = request.POST.get('vendedor_email')
        forma_pagamento = request.POST.get('forma_pagamento')

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
            forma_pagamento=forma_pagamento
        )

        for item in cart:
            product = item['product']
            quantity = int(item['quantity'])
            price = product.price * quantity

            item = OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)

        return redirect('myaccount')
    return redirect('cart')
