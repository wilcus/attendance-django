from django.shortcuts import render


def register(request):
    return render(request, 'register.html')


def registered(request):
    return render(request, 'registered.html')
