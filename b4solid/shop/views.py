import json
from turtle import up
from django.shortcuts import redirect, render
import requests as rq

def shop(request):

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

                rq.post(
                    url='http://aldenluth.fi:8081/orders',
                    data=json.dumps(updated_order),
                    headers={'Content-Type': 'application/json'}
                )

        return redirect('shop:shop')

    products_all = rq.get('http://aldenluth.fi:8082/products').json()
    orders_all = rq.get('http://aldenluth.fi:8081/orders/' + request.session['user']).json()

    context = {}
    context['products'] = products_all
    context['orders'] = sum(x['amount'] for x in orders_all)

    for product in products_all:
        product['id_label'] = f'#{product["id"]:08X}'

    return render(request, 'shop.html', context=context)
