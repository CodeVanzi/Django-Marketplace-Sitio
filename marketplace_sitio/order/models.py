from itertools import product
from django.contrib.auth.models import User
from django.db import models

from product.models import Product
from django.utils import timezone

class Order(models.Model):
    ORDERED = 'Pedido Realizado'
    SHIPPED = 'Pedido Saiu para Entrega'
    FINISHED = 'Pedido Concluído'

    STATUS_CHOICES = (
        (ORDERED, 'Pedido Realizado'),
        (SHIPPED, 'Pedido Enviado'),
        (FINISHED, 'Pedido Concluído')
    )
    
    card = 'Cartão de Crédito'
    boleto = 'Boleto'
    
    PAYMENT_CHOICES = (
        (card,'Cartão de Crédito'),
        (boleto,'Boleto'),
    )

    manha = 'Manhã'
    tarde = 'Tarde'
    
    HORA_CHOICES = (
        (manha,'Manhã'),
        (tarde,'Tarde'),
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    hora_entrega = models.CharField(max_length=255, choices=HORA_CHOICES, default=manha)
    data_entrega = models.DateField()
    vendedor_nome = models.CharField(max_length=255)
    telefone_vendedor = models.CharField(max_length=255)
    vendedor_email = models.CharField(max_length=255)
    forma_pagamento = models.CharField(max_length=255, choices=PAYMENT_CHOICES, default=card)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=9999) 
    payment_intent = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=1)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ORDERED)
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(blank=True, null=True, decimal_places=2, max_digits=9999)
    quantity = models.IntegerField(default=1)
    
    def get_total_price(self):
        return (self.price * self.quantity)