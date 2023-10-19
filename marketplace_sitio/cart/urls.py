from django.urls import path

from cart.views import update_menu_cart, cart, checkout, hx_menu_cart, update_cart


urlpatterns = [
    path('', cart, name='cart'),
    # path('cart_item/<int:product_id>', cart_item, name='cart_item'),
    path('update_menu_cart/<int:product_id>/<str:action>', update_menu_cart, name='update_menu_cart'),
    path('update_cart/<int:product_id>/<str:action>', update_cart, name='update_cart'),
    path('checkout/', checkout, name='checkout'),
    path('hx_menu_cart/', hx_menu_cart, name='hx_menu_cart'),
]