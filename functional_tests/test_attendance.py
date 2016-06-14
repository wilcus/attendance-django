from base import FunctionalTest
from register_attendance_student_page import RegisterStudentPage
from list_student_page import ListStudentPage
from django.test.utils import override_settings
from attendances.models import Course, Student
from django.contrib.auth import get_user_model, SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from django.conf.global_settings import SESSION_COOKIE_NAME
from django.conf import settings

User = get_user_model()


class AttendanceTest(FunctionalTest):
    # fixtures = ['pre_created_database.json']
    @override_settings(DEBUG=True)
    def test_see_list_of_students_of_course(self):
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
        session = SessionStore()
        session[SESSION_KEY] = professor.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session[HASH_SESSION_KEY] = professor.get_session_auth_hash()
        session.save()
        self.browser.get(self.live_server_url + "/fake/")
        self.browser.add_cookie(dict(
            name=SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

        register_student_page = RegisterStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the students avaible to register with course with id=1
        register_student_page.get("/attendances/register/1")
        register_student_page.register(john.name)
        list_student_page = ListStudentPage(self.browser, root_uri=self.live_server_url)

        # I want to see the list of my students
        list_student_page.get("/attendances/registered/1")
        students_registered = list_student_page.students_registered
        self.assertIn(john.name, students_registered)
