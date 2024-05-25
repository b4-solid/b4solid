import json
from django.shortcuts import redirect, render
from django.contrib import messages
import requests as rq
import hashlib

# Create your views here.
def login(request):
    if request.method == 'POST':
        body = {
            "username": request.POST["username"],
            "password": hashlib.sha256(request.POST["password"].encode()).hexdigest()
        }

        result = rq.post(
            url='http://aldenluth.fi:8085/login',
            data=json.dumps(body),
            headers={'Content-Type': 'application/json'}
        )

        if result.status_code == 200:
            result_dict = json.loads(result.text)

            request.session['user'] = result_dict["username"]
            request.session['godmode'] = result_dict["admin"] == 'true'

            return redirect('main:main')
        else:
            messages.error(request, result.text)

    return render(request, 'login.html')

def register(request):
    context = {}
    if request.method == 'POST':
        result = rq.post(
            url='http://aldenluth.fi:8085/register',
            data=json.dumps(request.POST),
            headers={'Content-Type': 'application/json'}
        )

        if result.status_code == 201:
            messages.success(request, "Account created successfully!")
            return redirect('authentication:login')
        else:
            messages.error(request, result.text)

    return render(request, 'register.html')

def logout(request):
    request.session.flush()
    return redirect('authentication:login')