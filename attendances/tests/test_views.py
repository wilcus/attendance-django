from django.test import TestCase


class RegisterPageTest(TestCase):
    def test_register_page_use_register_template(self):
        response = self.client.get('/attendances/register')
        self.assertTemplateUsed(response, 'register.html')

    def test_register_page_use_registered_template(self):
        response = self.client.get('/attendances/registered')
        self.assertTemplateUsed(response, 'registered.html')
