from django.test import TestCase, Client
from django.urls import reverse
from course.models import Student, Course


class TestViews(TestCase):
    def test_course_list_GET(self):
        assert 1 == 2
