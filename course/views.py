from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from random import choices

from .models import Course, Student
from .forms import CourseForm

def check_instructor(user, course):
    authorized_user = course.instructor
    if user != authorized_user:
        return redirect('login')
    pass

@login_required
def list_courses_view(request):
    user = request.user
    courses = Course.objects.filter(instructor=user)
    context = {
        'courses' : courses,
    }
    return render(request, 'course/list_courses.html', context)

@login_required
def course_view(request, course_id):
    user = request.user
    course = Course.objects.get(course_id=course_id)
    check_instructor(user, course)
    students = Student.objects.filter(course=course)
    if select_student_button(request):
        selected = select_student(students)
        context = {
            'selected' : selected,
            'students' : students,
        }
        return redirect('select_student_view', student_id=selected.pk)
    context = {
        'students' : students,
        'course' : course,
    }
    return render(request, 'course/list_students.html', context)

@login_required
def select_student_view(request, student_id):
    user = request.user
    student = Student.objects.get(pk=student_id)
    course = student.course
    students = [x for x in Student.objects.filter(course=course) if x != student]
    check_instructor(user, course)
    if request.method == 'POST':
        if refused_button(request):
            adjust_student_attempts(student, 1)
        if completed_button(request):
            adjust_student_attempts(student, -1)
        if student.attempts == 0:
            add_attempt_to_all(course)
        apply_assists(request)
        return redirect('course_view', course_id=course.course_id)
    context = {
        'selected' : student,
        'students' : students,
        'course' : course,
        }
    return render(request, 'course/select_student.html', context)

def adjust_student_attempts(student, amount):
    student.attempts += amount
    student.save()
    if student.attempts < 1:
        diff = 1 - student.attempts
        course = student.course
        adjust_all_student_attempts(course, diff)

def apply_assists(request):
    for student_id in request.POST.getlist('assists[]'):
        student = Student.objects.get(pk=student_id)
        adjust_student_attempts(student, -1)

def adjust_all_student_attempts(course, amount):
    students = Student.objects.filter(course=course)
    for student in students:
        student.attempts += amount
        student.save()

def add_attempt_to_all(course):
    students = Student.objects.filter(course=course)
    for student in students:
        student.attempts +=1
        student.save()

def select_student(students):
    attempts = [x.attempts for x in students]
    attempt_sum = sum(attempts)
    attempts = [x / attempt_sum for x in attempts]
    return choices(students, k=1, weights=attempts)[0]

def refused_button(request):
    return request.method == 'POST' and 'refused' in request.POST

def completed_button(request):
    return request.method == 'POST' and 'completed' in request.POST

def select_student_button(request):
    return request.method == 'POST' and 'select_student' in request.POST

@login_required
def edit_courses_view(request):
    user = request.user
    print(type(settings.AUTH_USER_MODEL))
    print(type(Course))
    CourseFormset = inlineformset_factory(
        User,
        Course,
        fields=('course_id',),
        extra=1
    )
    if request.method == 'POST':
        formset = CourseFormset(request.POST, instance=user)
        if formset.is_valid():
            formset.save()
    formset = CourseFormset(instance=user)
    context = {
        'formset' : formset
    }
    return render(request, 'course/edit_courses.html', context)

@login_required
def edit_students_view(request, course_id):
    course = Course.objects.get(course_id=course_id)
    user = request.user
    check_instructor(request, course)
    StudentFormset = inlineformset_factory(Course, Student, fields=('name', 'attempts',), extra=1)
    if request.method == 'POST':
        formset = StudentFormset(request.POST, instance=course)
        if formset.is_valid():
            formset.save()
    formset = StudentFormset(instance=course)
    context = {
        'formset' : formset,
        'course' : course
    }
    return render(request, 'course/edit_students.html', context)





