import datetime

from django.conf import settings
from django.conf.global_settings import SESSION_COOKIE_NAME
from django.contrib.auth import (BACKEND_SESSION_KEY, HASH_SESSION_KEY,
                                 SESSION_KEY, get_user_model)
from django.contrib.sessions.backends.db import SessionStore
from django.test.utils import override_settings
from django.utils import timezone

from attendances.models import Attendance, Course, Student
from attendances.views import SUCCESS_MESSAGE, FINISHED_COURSE_MESSAGE
from base import FunctionalTest
from course_list_page import CourseListPage
from list_link_date_page import ListLinkDatePage
from list_student_page import ListStudentPage
from login_page import LoginPage
from register_attendance_student_page import RegisterStudentPage

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
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
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
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        register_student_page.toggle_check(john.name)
        register_student_page.submit_button.click()
        list_student_page = ListStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the list of my students
        attendance = Attendance.objects.all()[0]
        list_student_page.get("/attendances/registered/{0}/{1:%Y-%m-%d}".format(course.pk, attendance.date))
        students_registered = list_student_page.students_registered
        self.assertIn(john.name, students_registered)

    def test_cannot_register_students_when_the_course_is_finished(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date() - datetime.timedelta(days=2),
            finish_date=timezone.now().date() - datetime.timedelta(days=1)
        )
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
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        finished_course_message = register_student_page.finished_course_message

        self.assertIn(finished_course_message, FINISHED_COURSE_MESSAGE)

    def test_see_list_of_link_of_dates_where_students_are_registered(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
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
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        register_student_page.toggle_check(john.name)
        register_student_page.submit_button.click()
        list_link_date_page = ListLinkDatePage(self.browser, root_uri=self.live_server_url)

        # I want to see the list of links
        attendance = Attendance.objects.all()[0]
        list_link_date_page.get("/attendances/registered-dates/{0}".format(course.pk))
        dates = list_link_date_page.dates
        self.assertIn("{0:%d %B %Y}".format(attendance.date), dates)

    def test_see_message_register_attendances_sucessfully(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
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
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        register_student_page.toggle_check(john.name)
        register_student_page.submit_button.click()
        self.assertEquals(register_student_page.success_message, SUCCESS_MESSAGE)

    def test_see_list_of_registered_students_in_form(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
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

    def test_not_see_list_of_registered_students_in_form_if_student_was_registered_2_days_before(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
        john = Student.objects.create(name="john")
        students_of_course = [
            john,
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        professor = User.objects.create(username="george")
        course.professors.add(professor)
        before_two_days_date = timezone.now() - datetime.timedelta(days=2)
        attendance = Attendance.objects.create(course=course, student=john)
        Attendance.objects.filter(pk=attendance.pk).update(date=before_two_days_date)

        self.create_preauthenticated_session_for(professor)
        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I don't want to see john student is checked in form
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        checked_students = register_student_page.checked_students
        self.assertNotIn(john.name, checked_students)

    def test_uncheck_student_in_form_should_not_appear_in_list_of_registered_students(self):
        # Given a database with students enrolled to courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
        john = Student.objects.create(name="john")
        students_of_course = [
            john,
            Student.objects.create(name="michael")
        ]
        course.students.add(*students_of_course)
        professor = User.objects.create(username="george")
        course.professors.add(professor)
        attendance = Attendance.objects.create(course=course, student=john)

        self.create_preauthenticated_session_for(professor)
        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)
        register_student_page.get("/attendances/register/{0}".format(course.pk))
        register_student_page.toggle_check(john.name)
        register_student_page.submit_button.click()
        list_student_page = ListStudentPage(self.browser, root_uri=self.live_server_url)

        list_student_page.get("/attendances/registered/{0}/{1:%Y-%m-%d}".format(course.pk, attendance.date))
        students_registered = list_student_page.students_registered
        self.assertNotIn(john.name, students_registered)

    def test_when_logged_go_to_course_list_page(self):
        # create a professor with courses
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
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
        # do not use page.get because is redirected in login
        course_list = course_list_page.course_list
        self.assertIn(course.name, course_list)

    def test_if_user_is_not_logged_and_want_register_page_go_to_login_page(self):
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )

        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)
        register_student_page.get("/attendances/register/{0}".format(course.pk))

        self.assertEquals(len(self.browser.find_elements_by_id('id_username')), 1)

    def test_if_user_is_not_logged_and_want_registered_page_go_to_login_page(self):
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )

        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)
        course = Course.objects.create(
            name="maths",
            start_date=timezone.now().date(),
            finish_date=timezone.now().date(),
        )
        register_student_page.get("/attendances/register/{0}".format(course.pk))

        self.assertEquals(len(self.browser.find_elements_by_id('id_username')), 1)
