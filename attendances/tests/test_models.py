from attendances.models import Student
import pytest


class TestStudent:
    @pytest.mark.django_db
    def test_get_create_students(self):
        Student.objects.create(name="John")
