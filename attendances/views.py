from django.shortcuts import render
from .forms import StudentListForm


def register(request, course):
    student_list_form = StudentListForm(course, request.user)
    return render(request, 'register.html', {'form': student_list_form})


def registered(request):
    return render(request, 'registered.html')
