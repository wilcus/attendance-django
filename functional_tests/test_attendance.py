from base import FunctionalTest
from register_attendance_student_page import RegisterStudentPage
from list_student_page import ListStudentPage
from django.test.utils import override_settings
from attendances.models import Course, Student


class AttendanceTest(FunctionalTest):
    # fixtures = ['pre_created_database.json']
    @override_settings(DEBUG=True)
    def test_see_list_of_students_of_course(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(name="maths")
        students_of_course = [
            Student.objects.create(name="john"),
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)

        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the students avaible to register with course with id=1
        register_student_page.get("/attendances/register/1")
        register_student_page.register("john")
        list_student_page = ListStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the list of my students
        list_student_page.get("/attendances/registered/1")
        students_registered = list_student_page.students_registered
        self.assertIn("John", students_registered)
