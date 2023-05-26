from django.shortcuts import render


# Create your views here.

# index page
def index(request):
    return render(request, 'delivery/index.html')


def cargo(request):
    return render(request, 'delivery/cargo.html', {'cargo': []})


def cars(request):
    return render(request, 'delivery/index.html')
