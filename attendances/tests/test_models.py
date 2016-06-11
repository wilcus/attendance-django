from attendances.models import Student, Course, Attendance
import pytest


class TestStudent:
    @pytest.mark.django_db
    def test_get_create_students(self):
        Student.objects.create(name="John")


class TestAttendance:
    @pytest.mark.django_db
    def test_get_create_attendance(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        Attendance.objects.create(student=student, course=course)
