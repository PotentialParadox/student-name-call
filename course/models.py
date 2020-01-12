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
    attempts = models.IntegerField(default=0, validators=[MaxValueValidator(1000), MinValueValidator(1)])
    assists = models.IntegerField(default=0, validators=[MaxValueValidator(1000), MinValueValidator(0)])
    weight = models.IntegerField(default=1, validators=[MaxValueValidator(100), MinValueValidator(0)])
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
    )

    def add_assist(self):
        self.assists += 1
        self.save()

    def add_attempt(self):
        self.attempts += 1
        self.save()

    def adjust_weight(self, amount):
        self.weight += amount
        self.save()
        if self.weight < 1:
            diff = 1 - self.weight
            self.adjust_all_student_weights(diff)

    def adjust_all_student_weights(self, amount):
        course = self.course
        students = Student.objects.filter(course=course)
        for student in students:
            student.adjust_weight(amount)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
