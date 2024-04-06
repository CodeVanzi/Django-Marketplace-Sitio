
from django.shortcuts import render, get_object_or_404
from .models import Product

def product(request, slug):
    """
    Renders the product page for a given product slug.
    """
    product_obj = get_object_or_404(Product, slug=slug)
    return render(request, 'product/product.html', {'product': product_obj})

