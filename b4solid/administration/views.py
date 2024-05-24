from django.shortcuts import render
import requests as rq

# Create your views here.
def requests(request):
    return render(request, 'requests.html')

def products(request):
    products_all = rq.get('http://aldenluth.fi:8082/products').json()

    context = {}
    context['products'] = products_all

    for product in products_all:
        product['id_label'] = f'#{product["id"]:08x}'

    if request.method == 'POST':
        rq.delete('http://aldenluth.fi/products/' + request.POST['id'])

    return render(request, 'products.html', context=context)