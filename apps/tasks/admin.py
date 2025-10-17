"""
Django Admin Configuration for Task Model
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Custom Task Admin"""
    
    list_display = [
        'id',
        'title',
        'user_email',
        'completed_status',
        'priority_badge',
        'due_date',
        'created_at',
    ]
    
    list_filter = [
        'completed',
        'priority',
        'created_at',
        'due_date',
        'user',
    ]
    
    search_fields = [
        'title',
        'description',
        'user__email',
        'user__username',
    ]
    
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'status',
        'is_overdue',
    ]
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Task Details', {
            'fields': ('priority', 'due_date', 'user')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'is_overdue', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    def user_email(self, obj):
        """Display user email"""
        return obj.user.email
    user_email.short_description = 'User'
    user_email.admin_order_field = 'user__email'
    
    def completed_status(self, obj):
        """Display completion status with color"""
        if obj.completed:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Completed</span>'
            )
        return format_html(
            '<span style="color: orange; font-weight: bold;">○ Pending</span>'
        )
    completed_status.short_description = 'Status'
    completed_status.admin_order_field = 'completed'
    
    def priority_badge(self, obj):
        """Display priority with colored badge"""
        colors = {
            'LOW': '#28a745',
            'MEDIUM': '#ffc107',
            'HIGH': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; '
            'border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.priority
        )
    priority_badge.short_description = 'Priority'
    priority_badge.admin_order_field = 'priority'
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user')
    
    actions = ['mark_as_completed', 'mark_as_pending']
    
    def mark_as_completed(self, request, queryset):
        """Admin action to mark tasks as completed"""
        updated = queryset.update(completed=True)
        self.message_user(
            request,
            f'{updated} task(s) marked as completed.'
        )
    mark_as_completed.short_description = 'Mark selected tasks as completed'
    
    def mark_as_pending(self, request, queryset):
        """Admin action to mark tasks as pending"""
        updated = queryset.update(completed=False)
        self.message_user(
            request,
            f'{updated} task(s) marked as pending.'
        )
    mark_as_pending.short_description = 'Mark selected tasks as pending'