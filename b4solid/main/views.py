from django.shortcuts import redirect, render

# Create your views here.
def main(request):
    if request.session.get('user', None) == None:
        return redirect('authentication:login')
    return render(request, 'home.html')