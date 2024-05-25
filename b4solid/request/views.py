from django.shortcuts import redirect, render
from django.contrib import messages
import requests as rq
import json

# Create your views here.
def user_requests(request):
    if 'user' not in request.session:
        return redirect('authentication:login')

    if request.method == 'POST':
        rq.delete('http://aldenluth.fi:8083/requests/' + request.POST['id'])

    user_requests = rq.get('http://aldenluth.fi:8083/requests/user/' + request.session['user'])
    user_requests = user_requests.json()

    context = {}
    context['requests'] = user_requests

    for req in user_requests:
        if req["productId"] is not None:
            req['product_label'] = f'#{req["productId"]:08X}'
        req['id_label'] = f'#{req["id"]:08X}'

    return render(request, 'user_requests.html', context=context)

def add_request(request):
    if 'user' not in request.session:
        return redirect('authentication:login')

    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'username': request.session['user']})

        rq.post(
            url='http://aldenluth.fi:8083/requests',
            data=json.dumps(updated_request),
            headers={'Content-Type': 'application/json'}
        )

        return redirect('request:user_requests')

    return render(request, 'add_request.html')

def edit_request(request, id):
    if 'user' not in request.session:
        return redirect('authentication:login')

    if request.method == 'POST':
        updated_request = request.POST.copy()
        updated_request.update({'username': request.session['user']})

        rq.put(
            url='http://aldenluth.fi:8083/requests/' + str(id),
            data=json.dumps(updated_request),
            headers={'Content-Type': 'application/json'}
        )
        return redirect('request:user_requests')

    req = rq.get('http://aldenluth.fi:8083/requests/' + str(id)).json()
    req['id_label'] = f'#{req["id"]:08X}'

    context = {}
    context['req'] = req

    return render(request, 'edit_request.html', context=context)
