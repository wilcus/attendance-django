from django.shortcuts import render
from .forms import RegisterStudentListForm


def register(request, course):
    student_list_form = RegisterStudentListForm(course=course, professor=request.user)
    return render(request, 'register.html', {'form': student_list_form})


def registered(request, course):
    students = []
    return render(request, 'registered.html', {'students': students})
