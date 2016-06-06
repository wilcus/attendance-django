from base import FunctionalTest
from register_attendance_student_page import RegisterStudentPage
from list_student_page import ListStudentPage


class AttendanceTest(FunctionalTest):
    # fixtures = ['pre_created_database.json']

    def test_see_list_of_students_of_course(self):
        # Given a database with students enrolled to courses
        # I want to see the list of my students
        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)
        register_student_page.get("/attendances/register")
        register_student_page.register("John")
        list_student_page = ListStudentPage(self.browser, root_uri=self.live_server_url)
        list_student_page.get("/attendances/registered")
        students_registered = list_student_page.students_registered
        self.assertIn("John", students_registered)
