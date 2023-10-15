
from django.contrib import admin
from django.urls import path

from cart.views import add_to_cart
from core.views import frontpage, shop, signup
from product.views import product

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', frontpage, name='frontpage'),
    path('shop/', shop, name='shop'),
    path('shop/<slug:slug>/', product, name='product'),
    path('cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('signup/', signup, name='signup')
]
