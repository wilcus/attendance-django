from django.shortcuts import render
from django.contrib.auth import get_user
from .forms import RegisterStudentListForm
from .models import Attendance


def register(request, course):
    assert request.user.is_authenticated(), "user no authenticated"

    student_list_form = RegisterStudentListForm(course=course, professor=get_user(request))
    return render(request, 'register.html', {'form': student_list_form})


def registered(request, course):
    students = Attendance.objects.filter(course=course, course__professors__in=[get_user(request)])
    return render(request, 'registered.html', {'students': students})
