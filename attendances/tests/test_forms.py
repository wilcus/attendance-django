from attendances.forms import RegisterStudentListForm
from unittest.mock import Mock, patch, ANY


class TestForms:
    @patch('attendances.forms.Student')
    def test_create_form(self, mock_Student):
        RegisterStudentListForm(course=ANY, professor=ANY)

    @patch('attendances.forms.Attendance')
    @patch('attendances.forms.Student')
    def test_save_attendances(self, mock_Student, mock_Attendance):
        student_list_form = RegisterStudentListForm(course=ANY, professor=ANY)
        student_list_form.cleaned_data = {}
        students_to_register = [Mock(pk=1, name="john"), Mock(pk=2, name="michael")]
        student_list_form.cleaned_data['students'] = students_to_register

        student_list_form.save()

        assert mock_Attendance.objects.create.call_count == len(students_to_register)
