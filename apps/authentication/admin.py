"""
Django Admin Configuration for User Model
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    
    list_display = [
        'email', 
        'username', 
        'first_name', 
        'last_name', 
        'role',
        'is_active', 
        'is_staff',
        'date_joined'
    ]
    list_filter = [
        'role', 
        'is_active', 
        'is_staff', 
        'is_superuser',
        'date_joined'
    ]
    search_fields = [
        'email', 
        'username', 
        'first_name', 
        'last_name'
    ]
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name')
        }),
        (_('Permissions'), {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions'
            )
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'role',
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
    )
    
    readonly_fields = ['date_joined', 'last_login']
    filter_horizontal = ['groups', 'user_permissions']