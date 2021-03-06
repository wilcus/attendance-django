from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    professors = models.ManyToManyField(settings.AUTH_USER_MODEL)
    start_date = models.DateField()
    finish_date = models.DateField()

    def __str__(self):
        return self.name


class Attendance(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    date = models.DateField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.student not in self.course.students.all():
            raise ValidationError("Can't register attendance of student not enrolled in course")
        super().save(*args, **kwargs)
