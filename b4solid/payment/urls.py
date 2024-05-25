from django.urls import include, path
from payment.views import cart, delete_order

app_name = 'payment'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('delete_order/<int:id>', delete_order, name='delete_order')
]