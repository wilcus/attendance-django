from unittest.mock import Mock, patch, ANY
from attendances.views import register
from django.test import TestCase


class UnpackArgsRenderMixin:
    def context(self, call_args):
        args, kwargs = call_args
        request_mock, template, context = args
        return context

    def template(self, call_args):
        args, kwargs = call_args
        request_mock, template, context = args
        return template


class TestRegisterPage(UnpackArgsRenderMixin):
    @patch('attendances.views.StudentListForm')
    @patch('attendances.views.render')
    def test_get_students_from_a_professor_and_course(self, mock_render, mock_StudentListForm, rf):
        request = rf.get('fake')
        request.user = Mock()
        mock_student_list_form = mock_StudentListForm.return_value

        register(request, ANY)

        context = self.context(mock_render.call_args)
        assert mock_student_list_form == context['form']

    @patch('attendances.views.StudentListForm')
    @patch('attendances.views.render')
    def test_register_page_use_register_template(self, mock_render, mock_StudentListForm, rf):
        request = rf.get('fake')
        request.user = Mock()

        register(request, ANY)

        template = self.template(mock_render.call_args)
        assert 'register.html' == template


class TestRouting(TestCase):
    def test_register_page_use_registered_template(self):
        response = self.client.get('/attendances/registered')
        self.assertTemplateUsed(response, 'registered.html')
