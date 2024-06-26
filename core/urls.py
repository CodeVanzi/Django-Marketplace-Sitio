from django.urls import path
from core.views import frontpage, signup, shop, myaccount, editmyaccount
from django.contrib.auth import views
from product.views import product

urlpatterns = [   
    path('', frontpage, name='frontpage'),
    path('signup/', signup, name='signup'),
    path('login/', views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('myaccount/', myaccount, name='myaccount'),
    path('myaccount/edit/', editmyaccount, name='editmyaccount'),
    path('shop/', shop, name='shop'),
    path('product/<slug:slug>/', product, name='product'),
    
]
