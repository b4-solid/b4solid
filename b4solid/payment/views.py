from datetime import datetime
import json
from django.shortcuts import redirect, render
import requests as rq

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

                rq.post(
                    url='http://aldenluth.fi:8081/orders',
                    data=json.dumps(updated_order),
                    headers={'Content-Type': 'application/json'}
                )

        return redirect('payment:cart')

    orders_all = rq.get('http://aldenluth.fi:8081/orders/' + request.session['user']).json()
    vouchers_all = rq.get('http://aldenluth.fi:8084/vouchers').json()

    context = {}
    context['orders'] = orders_all
    context['vouchers'] = vouchers_all

    for order in orders_all:
        product = rq.get('http://aldenluth.fi:8082/products/' + str(order["productId"])).json()
        order['product'] = product
        order['id_label'] = f'#{order["orderId"]:08X}'
        order['product_label'] = f'#{order["productId"]:08X}'

    return render(request, 'cart.html', context=context)

def delete_order(request, id):
    if 'user' not in request.session:
        return redirect('authentication:login')

    rq.delete('http://aldenluth.fi:8081/orders/' + str(id))

    return redirect('payment:cart')

def checkout(request):
    if 'user' not in request.session:
        return redirect('authentication:login')

    context = {}

    if request.method == 'POST':
        orders_all = rq.get('http://aldenluth.fi:8081/orders/' + request.session['user']).json()

        for order in orders_all:
            order['product'] = rq.get('http://aldenluth.fi:8082/products/' + str(order["productId"])).json()

        total_amount = sum([order['amount'] * order['product']['harga'] for order in orders_all])

        if 'voucher' in request.POST and request.POST['voucher'] != '0':
            voucher = rq.get('http://aldenluth.fi:8084/vouchers/' + request.POST['voucher']).json()

            voucher['noOfUsed'] += 1

            rq.put(
                url='http://aldenluth.fi:8084/vouchers/' + str(request.POST['voucher']),
                data=json.dumps(voucher),
                headers={'Content-Type': 'application/json'}
            )

            total_amount *= ((100 - voucher['discountAmount']) / 100)

        transaction = {
            'username': request.session['user'],
            'totalAmount': int(total_amount),
        }

        if 'voucher' in request.POST and request.POST['voucher'] != '0':
            transaction['voucherId'] = int(request.POST['voucher'])

        transaction_result = rq.post(
            url='http://aldenluth.fi:8080/transactions',
            data=json.dumps(transaction),
            headers={'Content-Type': 'application/json'}
        ).json()


        for order in orders_all:
            order['transactionId'] = transaction_result['id']
            rq.put(
                url='http://aldenluth.fi:8081/orders/' + str(order['orderId']),
                data=json.dumps(order),
                headers={'Content-Type': 'application/json'}
            )

            order['product']['stok'] = order['product']['stok'] - order['amount']
            rq.put(
                url='http://aldenluth.fi:8082/products/' + str(order['productId']),
                data=json.dumps(order['product']),
                headers={'Content-Type': 'application/json'}
            )

            invalid_orders = rq.get('http://aldenluth.fi:8081/orders/product/' + f"{order['product']['id']}/{order['product']['stok']}").json()
            print(invalid_orders)
            for invalid_order in invalid_orders:
                rq.delete('http://aldenluth.fi:8081/orders/' + str(invalid_order['orderId']))

        return redirect('payment:checkout')

    all_transactions = rq.get("http://aldenluth.fi:8080/transactions/user/" + request.session['user']).json()
    context['transactions'] = all_transactions

    for transaction in all_transactions:
        transaction['id_label'] = f'#{transaction["id"]:08X}'
        transaction['voucher_label'] = f'#{transaction["voucherId"]:08X}' if transaction["voucherId"] else None

    return render(request, 'transactions.html', context=context)
