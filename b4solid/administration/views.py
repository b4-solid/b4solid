import json
from django.shortcuts import redirect, render
from django.contrib import messages
import requests as rq


def requests(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        req = rq.get('http://aldenluth.fi:8083/requests/' +
                     request.POST['id']).json()

        created_product = {
            "nama": req['name'],
            "harga": req['harga'],
            "currency": "IDR",
            "deskripsi": req['deskripsi'],
            "stok": 1,
            "imageLink": req['imageLink']
        }

        if request.POST['action'] == 'approve':
            result = rq.post(
                url='http://aldenluth.fi:8082/products',
                data=json.dumps(created_product),
                headers={'Content-Type': 'application/json'}
            )

            result_dict = result.json()

            req['status'] = True
            req['productId'] = result_dict['id']

            result = rq.put(
                url='http://aldenluth.fi:8083/requests/' + request.POST['id'],
                data=json.dumps(req),
                headers={'Content-Type': 'application/json'}
            )

        elif request.POST['action'] == 'reject':
            print(req)
            req['status'] = False

            result = rq.put(
                url='http://aldenluth.fi:8083/requests/' + request.POST['id'],
                data=json.dumps(req),
                headers={'Content-Type': 'application/json'}
            )

            print(result.text)

    user_requests = rq.get('http://aldenluth.fi:8083/requests')
    user_requests = user_requests.json()

    context = {}
    context['requests'] = user_requests

    for req in user_requests:
        if req["productId"] is not None:
            req['product_label'] = f'#{req["productId"]:08X}'
        req['id_label'] = f'#{req["id"]:08X}'

    return render(request, 'requests.html', context=context)


def products(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        rq.delete('http://aldenluth.fi:8082/products/' + request.POST['id'])

    products_all = rq.get('http://aldenluth.fi:8082/products').json()

    context = {}
    context['products'] = products_all

    for product in products_all:
        product['id_label'] = f'#{product["id"]:08X}'

    return render(request, 'products.html', context=context)


def add_product(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        rq.post(
            url='http://aldenluth.fi:8082/products',
            data=json.dumps(request.POST),
            headers={'Content-Type': 'application/json'}
        )
        return redirect('administration:products')

    return render(request, 'add_product.html')


def edit_product(request, id):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        rq.put(
            url='http://aldenluth.fi:8082/products/' + str(id),
            data=json.dumps(request.POST),
            headers={'Content-Type': 'application/json'}
        )
        return redirect('administration:products')

    product = rq.get('http://aldenluth.fi:8082/products/' + str(id)).json()
    product['id_label'] = f'#{product["id"]:08X}'

    context = {}
    context['product'] = product

    return render(request, 'edit_product.html', context=context)


def vouchers(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        rq.delete('http://aldenluth.fi:8084/vouchers/' +
                  request.POST['voucherId'])

    vouchers_all = rq.get('http://aldenluth.fi:8084/vouchers').json()

    context = {}
    context['vouchers'] = vouchers_all

    for voucher in vouchers_all:
        voucher['id_label'] = f'#{voucher["voucherId"]:08X}'

    return render(request, 'vouchers.html', context=context)


def add_voucher(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        result = rq.post(
            url='http://aldenluth.fi:8084/vouchers',
            data=json.dumps(request.POST),
            headers={'Content-Type': 'application/json'}
        )

        if result.status_code == 201:
            return redirect('administration:vouchers')
        else:
            messages.error(request, result.text)

    return render(request, 'add_voucher.html')


def edit_voucher(request, id):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        result = rq.put(
            url='http://aldenluth.fi:8084/vouchers/' + str(id),
            data=json.dumps(request.POST),
            headers={'Content-Type': 'application/json'}
        )
        if result.status_code == 200:
            return redirect('administration:vouchers')
        else:
            messages.error(request, result.text)

    voucher = rq.get('http://aldenluth.fi:8084/vouchers/' + str(id)).json()
    voucher['id_label'] = f'#{voucher["voucherId"]:08X}'

    context = {}
    context['voucher'] = voucher

    return render(request, 'edit_voucher.html', context=context)
