from django import forms
import datetime
from .models import Student, Attendance


class RegisterStudentListForm(forms.Form):
    students = forms.ModelMultipleChoiceField(queryset=None, widget=forms.CheckboxSelectMultiple(), required=False)

    def __init__(self, course_id, professor, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.course_id = course_id
        self.fields['students'].queryset = Student.objects.filter(
            course__id=course_id,
            course__professors__in=[professor]
        )
        students_already_registered = Student.objects.filter(
            attendance__course_id=course_id,
            attendance__course__professors__in=[professor]
        )
        self.fields['students'].initial = [student.pk for student in students_already_registered]

    def save(self):
        students = self.cleaned_data['students']
        for student in students:
            if not Attendance.objects.filter(course_id=self.course_id, student=student).exists():
                Attendance.objects.create(course_id=self.course_id, student=student)
        for pk in self.fields['students'].initial:
            attendance = Attendance.objects.filter(course_id=self.course_id, student_id=pk, date=datetime.date.today())
            if attendance.exists():
                attendance.delete()
