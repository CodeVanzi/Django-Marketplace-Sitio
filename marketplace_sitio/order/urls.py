from django.urls import path

from .views import start_order, myorders

urlpatterns = [
    path('start_order/', start_order, name='start_order'),
    path('myorders/', myorders, name='myorders')
]