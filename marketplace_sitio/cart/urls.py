from django.urls import path

from cart.views import update_cart, cart, checkout, hx_menu_cart


urlpatterns = [
    path('', cart, name='cart'),
    path('update_cart/<int:product_id>/<str:action>', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
]