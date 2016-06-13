from django import forms
from .models import Student, Attendance


class RegisterStudentListForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=None)

    def __init__(self, course, professor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course = course
        self.fields['students'].queryset = Student.objects.filter(
            course=course,
            course__professors__in=[professor]
        )

    def save(self):
        students = self.cleaned_data['students']
        for student in students:
            Attendance.objects.create(course=self.course, student=student)
