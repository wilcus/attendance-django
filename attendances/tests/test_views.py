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
    @patch('attendances.views.Student')
    @patch('attendances.views.render')
    def test_get_students_from_a_professor(self, mock_render, mock_Student, rf):
        student = Mock(name="John")
        mock_Student.objects.filter.return_value = [student]
        request = rf.get('fake')

        register(request, ANY)

        context = self.context(mock_render.call_args)
        assert student in context['students']

    @patch('attendances.views.Student')
    @patch('attendances.views.render')
    def test_register_page_use_register_template(self, mock_render, mock_Student, rf):
        mock_Student.objects.all.return_value = Mock()
        request = rf.get('fake')

        register(request, ANY)

        template = self.template(mock_render.call_args)
        assert 'register.html' == template


class TestRouting(TestCase):
    def test_register_page_use_registered_template(self):
        response = self.client.get('/attendances/registered')
        self.assertTemplateUsed(response, 'registered.html')
