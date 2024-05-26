from django.urls import include, path
from payment.views import cart, delete_order, checkout

app_name = 'payment'

urlpatterns = [
    path('cart/', cart, name='cart'),
    path('checkout', checkout, name='checkout'),
    path('delete_order/<int:id>', delete_order, name='delete_order')
]