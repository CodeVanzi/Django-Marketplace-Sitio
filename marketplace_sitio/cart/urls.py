from django.urls import path

from cart.views import cart, checkout, hx_menu_cart, update_cart, hx_cart_total, success, remove_all_from_cart


urlpatterns = [
    path('', cart, name='cart'),
    path('update_cart/<int:product_id>/<str:action>', update_cart, name='update_cart'),
    path('remove/<int:product_id>', remove_all_from_cart, name='remove_all_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
    path('hx_cart_total/', hx_cart_total, name='hx_cart_total'),
    path('success/', success, name='success'),
]