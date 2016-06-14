from django.shortcuts import render
from django.contrib.auth import get_user
from .forms import RegisterStudentListForm
from .models import Attendance


def register(request, course_id):
    assert request.user.is_authenticated(), "user no authenticated"

    student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request))
    return render(request, 'register.html', {'form': student_list_form})


def registered(request, course_id):
    students = Attendance.objects.filter(course__id=course_id, course__professors__in=[get_user(request)])
    return render(request, 'registered.html', {'students': students})
