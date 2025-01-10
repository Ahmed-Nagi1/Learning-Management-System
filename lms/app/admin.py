from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *   

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'created_at', 'updated_at')
    search_fields = ('title', 'instructor__username')
    list_filter = ('created_at', 'updated_at')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'course', 'order')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'order')
    search_fields = ('title', 'module__title')
    list_filter = ('module',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed')
    search_fields = ('student__username', 'course__title')
    list_filter = ('enrolled_at', 'completed')

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'module')
    search_fields = ('title', 'module__title')
    list_filter = ('module',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'issued_at')
    search_fields = ('student__username', 'course__title')
    list_filter = ('issued_at',)
