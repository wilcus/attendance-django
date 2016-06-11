from attendances.models import Student, Course, Attendance
from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


class TestStudent:
    @pytest.mark.django_db
    def test_get_create_students(self):
        Student.objects.create(name="John")

    @pytest.mark.django_db
    def test_get_courses_from_a_student(self):
        student = Student.objects.create(name="John")
        courses = [
            Course.objects.create(name="science"),
            Course.objects.create(name="maths")
        ]
        for course in courses:
            student.course_set.add(course)
        assert student.course_set.all().count() == len(courses)


class TestAttendance:
    @pytest.mark.django_db
    def test_get_create_attendance(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        Attendance.objects.create(student=student, course=course)


class TestCourse:
    @pytest.mark.django_db
    def test_get_students_from_a_course(self):
        course = Course.objects.create(name="music")
        students_of_course = [
            Student.objects.create(name="john"),
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        assert course.students.all().count() == len(students_of_course)

    @pytest.mark.django_db
    def test_get_proffessor_from_a_course(self):
        course = Course.objects.create(name="music")
        students_of_course = [
            Student.objects.create(name="john"),
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        professor = User.objects.create(username="george")
        course.professors.add(professor)
        assert course.professors.all().count() == 1
