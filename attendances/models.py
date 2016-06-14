from django.db import models
from django.conf import settings


class Student(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(Student)
    professors = models.ManyToManyField(settings.AUTH_USER_MODEL)


class Attendance(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
