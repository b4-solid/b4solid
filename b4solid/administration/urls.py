from django.urls import path
from administration.views import requests, products, add_product, edit_product, vouchers, add_voucher, edit_voucher

app_name = 'administration'

urlpatterns = [
    path('requests/', requests, name='requests'),
    path('products/', products, name='products'),
    path('vouchers/', vouchers, name='vouchers'),
    path('add_product/', add_product, name='add_product'),
    path('edit_product/<int:id>/', edit_product, name='edit_product'),
    path('add_voucher/', add_voucher, name='add_voucher'),
    path('edit_voucher/<int:id>/', edit_voucher, name='edit_voucher')
]