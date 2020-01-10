from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Course(models.Model):
    course_id = models.IntegerField()
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return str(self.course_id)

    class Meta:
        ordering = ['course_id']

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('course_view', args=[str(self.course_id)])


class Student(models.Model):
    name = models.CharField(max_length=20)
    attempts = models.IntegerField(default=10, validators=[MaxValueValidator(100), MinValueValidator(1)])
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
