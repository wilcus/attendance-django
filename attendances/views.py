from django.shortcuts import render
from .models import Student


def register(request, profesor):
    students = Student.objects.filter(profesor=profesor)
    return render(request, 'register.html', {'students': students})


def registered(request):
    return render(request, 'registered.html')
