from django.contrib import admin

# Register your models here.

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'zipcode', 'cidade', 'paid', 'created_at', 'forma_pagamento', 'vendedor_nome', 'status' ]
    list_filter = ['paid', 'created_at', 'status']
    search_fields = ['id', 'first_name', 'last_name', 'email', 'address', 'zipcode', 'cidade', 'phone', 'hora_entrega', 'data_entrega', 'vendedor_nome', 'telefone_vendedor', 'vendedor_email', 'forma_pagamento', 'status']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)