import json
from django.shortcuts import redirect, render
from django.contrib import messages
import requests
import hashlib

# Create your views here.
def login(request):
    if request.method == 'POST':
        body = {
            "username": request.POST["username"],
            "password": hashlib.sha256(request.POST["password"].encode()).hexdigest()
        }

        result = requests.post(
            url='http://127.0.0.1:8085/login',
            data=json.dumps(body),
            headers={'Content-Type': 'application/json'}
        )

        result_dict = json.loads(result.text)
        print(result_dict)
        if result_dict["status"] == "success":
            request.session['user'] = result_dict["username"]
            request.session['godmode'] = result_dict["admin"]
            return redirect('main:main')
        else:
            messages.error(request, result_dict["reason"])
    return render(request, 'login.html')

def register(request):
    context = {}
    if request.method == 'POST':
        result = requests.post(
            url='http://127.0.0.1:8085/register',
            data=json.dumps(request.POST),
            headers={'Content-Type': 'application/json'}
        )

        result_dict = json.loads(result.text)
        if result_dict["status"] == "success":
            messages.success(request, "Account created successfully!")
            return redirect('authentication:login')
        else:
            messages.error(request, result_dict["reason"])

    return render(request, 'register.html')

def logout(request):
    request.session.flush()
    return redirect('authentication:login')