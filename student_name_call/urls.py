"""student_name_call URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include # new
from pages.views import homepage_view, signup_view
from course.views import list_courses_view, course_view, edit_students_view, select_student_view
from course.views import edit_courses_view

urlpatterns = [
    path('', homepage_view, name='home'),
    path('admin/', admin.site.urls),
    path('signup/', signup_view, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', list_courses_view, name='courses'),
    path('accounts/profile/edit', edit_courses_view, name='edit_courses_view'),
    path('courses/<course_id>/', course_view, name='course_view'),
    path('select/<student_id>', select_student_view, name='select_student_view'),
    path('courses/<course_id>/edit', edit_students_view, name='edit_students'),
]
