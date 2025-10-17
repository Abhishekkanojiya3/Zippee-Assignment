"""
Task URL Configuration
"""

from django.urls import path
from .views import (
    TaskListCreateView,
    TaskDetailView,
    TaskStatusToggleView,
    TaskStatsView,
)

app_name = 'tasks'

urlpatterns = [
    # Task CRUD operations
    path('', TaskListCreateView.as_view(), name='task_list_create'),
    path('<int:id>/', TaskDetailView.as_view(), name='task_detail'),
    
    # Additional task operations
    path('<int:id>/toggle/', TaskStatusToggleView.as_view(), name='task_toggle'),
    path('stats/', TaskStatsView.as_view(), name='task_stats'),
]