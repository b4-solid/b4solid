from django.shortcuts import render
import requests as rq

# Create your views here.
def requests(request):
    return render(request, 'requests.html')

def products(request):

    if request.method == 'POST':
        rq.delete('http://aldenluth.fi:8082/products/' + request.POST['id'])

    products_all = rq.get('http://aldenluth.fi:8082/products').json()

    context = {}
    context['products'] = products_all

    for product in products_all:
        product['id_label'] = f'#{product["id"]:08x}'

    return render(request, 'products.html', context=context)