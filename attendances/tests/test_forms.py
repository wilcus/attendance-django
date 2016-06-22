from attendances.forms import RegisterStudentListForm
from unittest.mock import Mock, patch, ANY


class TestForms:
    @patch('attendances.forms.Student')
    def test_create_form(self, mock_Student):
        RegisterStudentListForm(course_id=ANY, professor=ANY)

    @patch('attendances.forms.Attendance')
    @patch('attendances.forms.Student')
    def test_save_attendances(self, mock_Student, mock_Attendance):
        student_list_form = RegisterStudentListForm(course_id=ANY, professor=ANY)
        student_list_form.cleaned_data = {}
        students_to_register = [Mock(pk=1, name="john"), Mock(pk=2, name="michael")]
        student_list_form.cleaned_data['students'] = students_to_register
        mock_Attendance.objects.filter.return_value.exists.return_value = False

        student_list_form.save()

        assert mock_Attendance.objects.create.call_count == len(students_to_register)

    @patch('attendances.forms.Attendance')
    @patch('attendances.forms.Student')
    def test_do_not_save_attendances_when_is_already_saved(self, mock_Student, mock_Attendance):
        student_list_form = RegisterStudentListForm(course_id=ANY, professor=ANY)
        student_list_form.cleaned_data = {}
        students_to_register = [Mock(pk=1, name="john"), Mock(pk=2, name="michael")]
        student_list_form.cleaned_data['students'] = students_to_register
        mock_Attendance.objects.filter.return_value.exists.return_value = True

        student_list_form.save()

        assert mock_Attendance.objects.create.call_count == 0

    @patch('attendances.forms.Attendance')
    @patch('attendances.forms.Student')
    def test_if_student_is_unchecked_and_is_registered_then_delete_attendance(self, mock_Student, mock_Attendance):
        student_registered = Mock(pk=1, name="john")
        student_list_form = RegisterStudentListForm(course_id=ANY, professor=ANY)
        student_list_form.cleaned_data = {}
        student_list_form.fields['students'].initial = [student_registered.pk]
        student_list_form.cleaned_data['students'] = []
        mock_Attendance.objects.filter.return_value = student_registered

        student_list_form.save()

        assert student_registered.delete.call_count == 1
