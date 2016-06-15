from attendances.models import Student, Course, Attendance
from django.contrib.auth import get_user_model
import pytest

User = get_user_model()


@pytest.mark.django_db
class TestStudent:
    def test_get_create_students(self):
        Student.objects.create(name="John")

    def test_get_courses_from_a_student(self):
        student = Student.objects.create(name="John")
        courses = [
            Course.objects.create(name="science"),
            Course.objects.create(name="maths")
        ]
        for course in courses:
            student.course_set.add(course)
        assert student.course_set.all().count() == len(courses)

    def test_get_students_from_a_professor_and_course(self):
        john = Student.objects.create(name="John")
        professor = User.objects.create(username="Mark")
        course = Course.objects.create(name="science")
        course.professors.add(professor)
        john.course_set.add(course)
        students = Student.objects.filter(
            course=course,
            course__professors__in=[professor]
        )
        assert len(students) == 1


@pytest.mark.django_db
class TestAttendance:
    def test_get_create_attendance(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        Attendance.objects.create(student=student, course=course)

    def test_get_create_attendance_with_id(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        Attendance.objects.create(course_id=course.id, student=student)


@pytest.mark.django_db
class TestCourse:
    def test_get_students_from_a_course(self):
        course = Course.objects.create(name="music")
        students_of_course = [
            Student.objects.create(name="john"),
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        assert course.students.all().count() == len(students_of_course)

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
