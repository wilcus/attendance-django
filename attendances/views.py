from django.shortcuts import render
from .forms import RegisterStudentListForm


def register(request, course):
    student_list_form = RegisterStudentListForm(course, request.user)
    return render(request, 'register.html', {'form': student_list_form})


def registered(request):
    return render(request, 'registered.html')
