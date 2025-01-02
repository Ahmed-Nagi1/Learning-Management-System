from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # تخصيص الحقول
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('email', 'full_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'full_name', 'role'),
        }),
    )

    list_display = ('username', 'email', 'full_name', 'role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

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
