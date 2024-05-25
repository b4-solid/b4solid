import json
from django.shortcuts import redirect, render
from django.contrib import messages
import requests as rq

def requests(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    return render(request, 'requests.html')

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
    print(product)

    context = {}
    context['product'] = product

    return render(request, 'edit_product.html', context=context)

def vouchers(request):
    if not request.session.get('godmode'):
        return redirect('main:main')

    if request.method == 'POST':
        rq.delete('http://aldenluth.fi:8084/vouchers/' + request.POST['voucherId'])

    vouchers_all = rq.get('http://aldenluth.fi:8084/vouchers').json()

    context = {}
    context['vouchers'] = vouchers_all
    print(vouchers_all)

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
    print(voucher)

    context = {}
    context['voucher'] = voucher

    return render(request, 'edit_voucher.html', context=context)