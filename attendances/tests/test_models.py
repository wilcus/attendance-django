from attendances.models import Student, Course, Attendance
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import datetime
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

    def test_get_students_with_attendance(self):
        john = Student.objects.create(name="John")
        professor = User.objects.create(username="Mark")
        course = Course.objects.create(name="science")
        course.professors.add(professor)
        john.course_set.add(course)
        Attendance.objects.create(course=course, student=john)
        students_with_attendance = Student.objects.filter(attendance__course_id=course.id, attendance__course__professors__in=[professor])
        assert len(students_with_attendance) == 1

    def test_get_students_with_attendance_in_a_date(self):
        john = Student.objects.create(name="John")
        professor = User.objects.create(username="Mark")
        course = Course.objects.create(name="science")
        course.professors.add(professor)
        john.course_set.add(course)
        attendance = Attendance.objects.create(course=course, student=john)
        day_after_tomorrow = attendance.date + datetime.timedelta(days=2)
        students_with_attendance = Student.objects.filter(
            attendance__course_id=course.id,
            attendance__course__professors__in=[professor],
            attendance__date=day_after_tomorrow
        )
        assert len(students_with_attendance) == 0

    def test_students_with_attendance_if_not_register_in_course(self):
        john = Student.objects.create(name="John")
        professor = User.objects.create(username="Mark")
        course = Course.objects.create(name="science")
        course.professors.add(professor)
        with pytest.raises(ValidationError):
            Attendance.objects.create(course=course, student=john)


@pytest.mark.django_db
class TestAttendance:
    def test_get_create_attendance(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        course.students.add(student)
        Attendance.objects.create(student=student, course=course)

    def test_get_create_attendance_with_id(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        course.students.add(student)
        Attendance.objects.create(course_id=course.id, student=student)

    def test_get_dates_from_a_course_and_professor(self):
        student = Student.objects.create(name="John")
        course = Course.objects.create(name="maths")
        course.students.add(student)
        professor = User.objects.create(username="Mark")
        course.professors.add(professor)
        Attendance.objects.create(course_id=course.id, student=student)
        dates = Attendance.objects.filter(course_id=course.id, course__professors__in=[professor]).only('date').distinct().order_by('date')
        assert dates.count() == 1


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
