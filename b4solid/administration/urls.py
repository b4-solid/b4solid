from django.urls import path
from administration.views import requests, products

app_name = 'administration'

urlpatterns = [
    path('requests/', requests, name='requests'),
    path('products/', products, name='products'),
]