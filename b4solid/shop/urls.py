from django.urls import include, path
from shop.views import shop

app_name = 'shop'

urlpatterns = [
    path('shop/', shop, name='shop'),
]