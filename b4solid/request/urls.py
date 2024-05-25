from django.urls import path
from request.views import user_requests, add_request, edit_request

app_name = 'request'

urlpatterns = [
    path('user_requests/', user_requests, name='user_requests'),
    path('add_request/', add_request, name='add_request'),
    path('edit_request/<int:id>/', edit_request, name='edit_request'),
]