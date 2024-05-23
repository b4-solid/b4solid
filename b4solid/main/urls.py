from django.urls import include, path
from main.views import main

app_name = 'main'

urlpatterns = [
    path('', main, name='main'),
]