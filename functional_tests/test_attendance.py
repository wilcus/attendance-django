from base import FunctionalTest
from register_attendance_student_page import RegisterStudentPage
from list_student_page import ListStudentPage
from course_list_page import CourseListPage
from login_page import LoginPage
from attendances.views import SUCCESS_MESSAGE
from django.test.utils import override_settings
from attendances.models import Course, Student, Attendance
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.conf.global_settings import SESSION_COOKIE_NAME
from django.conf import settings

User = get_user_model()


@override_settings(DEBUG=True)
class AttendanceTest(FunctionalTest):
    def create_preauthenticated_session_for(self, user):
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = user.get_session_auth_hash()
        session.save()
        self.browser.get(self.live_server_url + "/fake/")
        self.browser.add_cookie(dict(
            name=SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_see_list_of_registered_students_from_a_course(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(name="maths")
        john = Student.objects.create(name="john")
        students_of_course = [
            john,
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        professor = User.objects.create(username="george")
        course.professors.add(professor)

        self.create_preauthenticated_session_for(professor)

        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the students avaible to register with course with id=1
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        register_student_page.register(john.name)
        list_student_page = ListStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the list of my students
        list_student_page.get("/attendances/registered/{0}".format(course.pk))
        students_registered = list_student_page.students_registered
        self.assertIn(john.name, students_registered)

    def test_see_message_register_attendances_sucessfully(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(name="maths")
        john = Student.objects.create(name="john")
        students_of_course = [
            john,
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        professor = User.objects.create(username="george")
        course.professors.add(professor)

        self.create_preauthenticated_session_for(professor)
        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the students avaible to register with course with id=1
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        register_student_page.register(john.name)
        self.assertEquals(register_student_page.success_message, SUCCESS_MESSAGE)

    def test_see_list_of_registered_students_in_form(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(name="maths")
        john = Student.objects.create(name="john")
        students_of_course = [
            john,
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        professor = User.objects.create(username="george")
        course.professors.add(professor)
        Attendance.objects.create(course=course, student=john)

        self.create_preauthenticated_session_for(professor)

        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see john student is checked in form
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        checked_students = register_student_page.checked_students
        self.assertIn(john.name, checked_students)

    def test_when_logged_go_to_course_list_page(self):
        # create a professor with courses
        course = Course.objects.create(name="maths")
        professor = User.objects.create(username="george")
        password = "superpass"
        professor.set_password(password)
        professor.save()
        course.professors.add(professor)

        login_page = LoginPage(self.browser, root_uri=self.live_server_url)
        login_page.get("/login")
        login_page.username = professor.username
        login_page.password = password
        login_page.login.click()

        course_list_page = CourseListPage(self.browser, root_uri=self.live_server_url)
        # do not us page.get because is redirecter in login
        course_list = course_list_page.course_list
        self.assertIn(course.name, course_list)

    def test_if_user_is_not_logged_and_want_register_page_go_to_login_page(self):
        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the students avaible to register with course with id=1
        fake_course_id = 1
        register_student_page.get("/attendances/register/{0}".format(fake_course_id))

        self.assertEquals(len(self.browser.find_elements_by_id('id_username')), 1)

    def test_if_user_is_not_logged_and_want_registered_page_go_to_login_page(self):
        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the students avaible to register with course with id=1
        fake_course_id = 1
        register_student_page.get("/attendances/register/{0}".format(fake_course_id))

        self.assertEquals(len(self.browser.find_elements_by_id('id_username')), 1)
