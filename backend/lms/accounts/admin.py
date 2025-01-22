from django.contrib import admin
from .models import *


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

    # تخصيص الحقول
    fieldsets = (
        ('Personal Info', {'fields': ('email', 'full_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('password1', 'password2', 'email', 'full_name', 'role'),
        }),
    )

    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    search_fields = ('email', 'full_name')

admin.site.register(CustomUser, CustomUserAdmin)
