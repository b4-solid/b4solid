import json
from django.shortcuts import redirect, render
import requests as rq

# Create your views here.

def cart(request):

    if 'user' not in request.session:
        return redirect('authentication:login')

    if request.method == 'POST':
        request_data = {int(k):int(v) for k, v in request.POST.items() if k != 'csrfmiddlewaretoken' and v != '0'}

        for product_id, amount in request_data.items():
            if amount > 0:
                updated_order = {
                    'username': request.session['user'],
                    'productId': product_id,
                    'amount': amount
                }

                res = rq.post(
                    url='http://aldenluth.fi:8081/orders',
                    data=json.dumps(updated_order),
                    headers={'Content-Type': 'application/json'}
                )


                print(res.text)

        return redirect('payment:cart')

    orders_all = rq.get('http://aldenluth.fi:8081/orders/' + request.session['user']).json()

    context = {}
    context['orders'] = orders_all

    for order in orders_all:
        product = rq.get('http://aldenluth.fi:8082/products/' + str(order["productId"])).json()
        order['product'] = product
        order['id_label'] = f'#{order["orderId"]:08X}'
        order['product_label'] = f'#{order["productId"]:08X}'

    return render(request, 'cart.html', context=context)

def delete_order(request, id):
    res = rq.delete('http://aldenluth.fi:8081/orders/' + str(id))

    return redirect('payment:cart')
