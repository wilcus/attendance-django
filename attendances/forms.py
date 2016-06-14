from django import forms
from .models import Student, Attendance


class RegisterStudentListForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple())

    def __init__(self, course_id, professor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_id = course_id
        self.fields['students'].queryset = Student.objects.filter(
            course__id=course_id,
            course__professors__in=[professor]
        )

    def save(self):
        students = self.cleaned_data['students']
        for student in students:
            Attendance.objects.create(course__id=self.course_id, student=student)
