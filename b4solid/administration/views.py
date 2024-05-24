import json
from django.shortcuts import redirect, render
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

    context = {}
    context['product'] = product

    return render(request, 'edit_product.html', context=context)