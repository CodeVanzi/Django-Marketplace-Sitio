from django.urls import path

from .views import dashboard, db_cogumelos_view


urlpatterns = [
    path('dashboard/', dashboard, name='db_commodities'),
    path('db_cogumelos', db_cogumelos_view, name='db_cogumelos')
]