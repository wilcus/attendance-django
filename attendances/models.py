from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100)


class Student(models.Model):
    name = models.CharField(max_length=100)


class Attendance(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
