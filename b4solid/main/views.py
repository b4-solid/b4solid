from django.shortcuts import redirect, render

# Create your views here.
def main(request):
    if 'user' not in request.session:
        return redirect('authentication:login')

    context = {
        'user': request.session.get('user')
    }

    return render(request, 'main.html', context=context)