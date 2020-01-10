from django.contrib import admin
from .models import Course, Student

# Register your models here.
class StudentInline(admin.TabularInline):
    model = Student

class CourseAdmin(admin.ModelAdmin):
    inlines = [StudentInline]
    model = Course

admin.site.register(Course, CourseAdmin)
