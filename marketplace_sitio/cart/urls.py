from django.urls import path

from cart.views import update_menu_cart, cart, checkout, hx_menu_cart, update_cart, hx_cart_total


urlpatterns = [
    path('', cart, name='cart'),
    path('update_menu_cart/<int:product_id>/<str:action>', update_menu_cart, name='update_menu_cart'),
    path('update_cart/<int:product_id>/<str:action>', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', hx_cart_total, name='hx_cart_total'),
]