from itertools import product
from django.contrib.auth.models import User
from django.db import models

from product.models import Product
from django.utils import timezone

class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped')
    )

    user = models.ForeignKey(User, related_name='orders', blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    hora_entrega = models.CharField(max_length=255)
    data_entrega = models.DateField()
    vendedor_nome = models.CharField(max_length=255)
    telefone_vendedor = models.CharField(max_length=255)
    vendedor_email = models.CharField(max_length=255)
    forma_pagamento = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.IntegerField(blank=True, null=True) #confirmar se precisa mesmo ser integer, talvez precise revisar o código pq os produtos estão em decimal
    quantity = models.IntegerField(default=1)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)
    
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.IntegerField() #confirmar se precisa mesmo ser integer, talvez precise revisar o código pq os produtos estão em decimal
    quantity = models.IntegerField(default=1)