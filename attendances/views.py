from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from .forms import RegisterStudentListForm
from .models import Attendance, Course, Student

SUCCESS_MESSAGE = "You saved succesfully the attendances"
FINISHED_COURSE_MESSAGE = "This course is finished"
NOT_STARTED_COURSE_MESSAGE = "This course is not started"


def course_active(function):
    def wrapper(request, course_id):
        course = Course.objects.get(pk=course_id)
        if course.start_date > timezone.now().date() or course.finish_date < timezone.now().date():
            if course.start_date > timezone.now().date():
                return render(request, 'register.html', {'NOT_STARTED_COURSE_MESSAGE': NOT_STARTED_COURSE_MESSAGE})
            else:
                return render(request, 'register.html', {'FINISHED_COURSE_MESSAGE': FINISHED_COURSE_MESSAGE})
        else:
            return function(request, course_id)
    return wrapper


@course_active
@login_required
def register(request, course_id):
    course = Course.objects.get(pk=course_id)
    student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request))
    if request.method == 'POST':
        student_list_form = RegisterStudentListForm(course_id=course_id, professor=get_user(request), data=request.POST)
        if student_list_form.is_valid():
            student_list_form.save()
            messages.info(request, SUCCESS_MESSAGE)
        return render(request, 'register.html', {'course': course, 'form': student_list_form})
    return render(request, 'register.html', {'course': course, 'form': student_list_form})


@login_required
def registered(request, course_id, date):
    course = Course.objects.get(pk=course_id)
    students = Student.objects.filter(
        attendance__course__id=course_id,
        attendance__course__professors__in=[get_user(request)],
        attendance__date=date
    )
    date_ = timezone.datetime.strptime(date, "%Y-%m-%d").date()
    return render(request, 'registered.html', {'students': students, 'course': course, 'date_': date_})


@login_required
def registered_dates(request, course_id):
    course = Course.objects.get(pk=course_id)
    attendance_dates = Attendance.objects.filter(course_id=course_id, course__professors__in=[get_user(request)]).only('date').distinct().order_by('date')
    return render(request, 'registered_dates.html', {'attendance_dates': attendance_dates, 'course': course})


@login_required
def courses(request):
    courses = Course.objects.filter(professors__in=[get_user(request)])
    return render(request, 'courses.html', {'courses': courses})
