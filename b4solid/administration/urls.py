from django.urls import path
from administration.views import requests, products, add_product, edit_product

app_name = 'administration'

urlpatterns = [
    path('requests/', requests, name='requests'),
    path('products/', products, name='products'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:id>/', edit_product, name='edit_product')
]