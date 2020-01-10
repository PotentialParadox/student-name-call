from django import forms
from django.forms import inlineformset_factory

from .models import Course, Student

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = (
            'course_id',
        )
