"""
Task Filters
"""

from django_filters import rest_framework as filters
from django.db import models
from .models import Task


class TaskFilter(filters.FilterSet):
    """
    Filter class for Task model
    Provides filtering options for tasks
    """
    
    # Filter by completion status
    completed = filters.BooleanFilter(
        field_name='completed',
        help_text='Filter by completion status (true/false)'
    )
    
    # Filter by priority
    priority = filters.ChoiceFilter(
        field_name='priority',
        choices=Task._meta.get_field('priority').choices,
        help_text='Filter by priority (LOW, MEDIUM, HIGH)'
    )
    
    # Filter by date range
    created_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text='Filter tasks created after this date'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text='Filter tasks created before this date'
    )
    
    # Filter by due date
    due_after = filters.DateTimeFilter(
        field_name='due_date',
        lookup_expr='gte',
        help_text='Filter tasks due after this date'
    )
    due_before = filters.DateTimeFilter(
        field_name='due_date',
        lookup_expr='lte',
        help_text='Filter tasks due before this date'
    )
    
    # Filter overdue tasks
    overdue = filters.BooleanFilter(
        method='filter_overdue',
        help_text='Filter overdue tasks (true/false)'
    )
    
    class Meta:
        model = Task
        fields = {
            'completed': ['exact'],
            'priority': ['exact'],
            'created_at': ['gte', 'lte'],
            'due_date': ['gte', 'lte'],
        }

    
    def filter_overdue(self, queryset, name, value):
        """
        Filter overdue tasks
        """
        from django.utils import timezone
        
        if value:
            # Get tasks that are overdue (due_date < now and not completed)
            return queryset.filter(
                due_date__lt=timezone.now(),
                completed=False
            )
        else:
            # Get tasks that are not overdue
            return queryset.filter(
                models.Q(due_date__gte=timezone.now()) |
                models.Q(due_date__isnull=True) |
                models.Q(completed=True)
            )
