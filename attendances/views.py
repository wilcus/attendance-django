from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import RegisterStudentListForm
from .models import Attendance, Course, Student

SUCCESS_MESSAGE = "You saved succesfully the attendances"
FINISHED_COURSE_MESSAGE = "This course is finished"


@login_required
def register(request, course_id):
    student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request))
    if request.method == 'POST':
        student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request), data=request.POST)
        if student_list_form.is_valid():
            student_list_form.save()
            messages.info(request, SUCCESS_MESSAGE)
        return render(request, 'register.html', {'course_id': course_id, 'form': student_list_form})
    return render(request, 'register.html', {'course_id': course_id, 'form': student_list_form})


@login_required
def registered(request, course_id, date):
    students = Student.objects.filter(
        attendance__course__id=course_id,
        attendance__course__professors__in=[get_user(request)],
        attendance__date=date
    )
    return render(request, 'registered.html', {'students': students})


@login_required
def registered_dates(request, course_id):
    course = Course.objects.get(pk=course_id)
    attendance_dates = Attendance.objects.filter(course_id=course_id, course__professors__in=[get_user(request)]).only('date').distinct().order_by('date')
    return render(request, 'registered_dates.html', {'attendance_dates': attendance_dates, 'course': course})


@login_required
def courses(request):
    courses = Course.objects.filter(professors__in=[get_user(request)])
    return render(request, 'courses.html', {'courses': courses})
