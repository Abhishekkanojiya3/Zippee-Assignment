"""
Task Views - CRUD Operations
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from django.db.models import Q, Count

from .models import Task
from .serializers import (
    TaskSerializer,
    TaskCreateSerializer,
    TaskUpdateSerializer,
    TaskListSerializer,
    TaskStatusUpdateSerializer,
    TaskStatsSerializer,
)
from .filters import TaskFilter
from apps.authentication.permissions import IsOwnerOrAdmin


class TaskListCreateView(generics.ListCreateAPIView):
    """
    Task List and Create Endpoint
    
    GET: Retrieve a list of all tasks for authenticated user
    POST: Create a new task
    """
    
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'due_date', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Return tasks for current user only
        Admins can see all tasks
        """
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(user=user)
    
    def get_serializer_class(self):
        """
        Use different serializers for list and create
        """
        if self.request.method == 'POST':
            return TaskCreateSerializer
        return TaskListSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        # Return full task details
        response_serializer = TaskSerializer(task)
        return Response(
            {
                'message': 'Task created successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Task Detail, Update, and Delete Endpoint
    
    GET: Retrieve details of a specific task
    PUT/PATCH: Update a specific task
    DELETE: Delete a specific task
    """
    
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    lookup_field = 'id'
    
    def get_queryset(self):
        """
        Return tasks for current user only
        Admins can access all tasks
        """
        user = self.request.user
        if user.is_admin:
            return Task.objects.all()
        return Task.objects.filter(user=user)
    
    def get_serializer_class(self):
        """
        Use different serializers for different methods
        """
        if self.request.method in ['PUT', 'PATCH']:
            return TaskUpdateSerializer
        return TaskSerializer
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        response_serializer = TaskSerializer(task)
        return Response(
            {
                'message': 'Task updated successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        
        response_serializer = TaskSerializer(task)
        return Response(
            {
                'message': 'Task updated successfully',
                'data': response_serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(
            {'message': 'Task deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


class TaskStatusToggleView(APIView):
    """
    Toggle Task Completion Status
    
    POST: Toggle completion status of a task
    """
    
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def post(self, request, id):
        user = request.user
        
        # Get task (user-specific or all for admin)
        if user.is_admin:
            task = get_object_or_404(Task, id=id)
        else:
            task = get_object_or_404(Task, id=id, user=user)
        
        # Toggle completion status
        task.completed = not task.completed
        task.save()
        
        serializer = TaskSerializer(task)
        return Response(
            {
                'message': f'Task marked as {"completed" if task.completed else "incomplete"}',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )


class TaskStatsView(APIView):
    """
    Task Statistics Endpoint
    
    GET: Get statistics about user's tasks
    """
    
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        user = request.user
        
        # Get user's tasks (or all tasks for admin)
        if user.is_admin:
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(user=user)
        
        # Calculate statistics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(completed=True).count()
        pending_tasks = tasks.filter(completed=False).count()
        overdue_tasks = tasks.filter(
            due_date__lt=timezone.now(),
            completed=False
        ).count()
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        stats = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round(completion_rate, 2)
        }
        
        serializer = TaskStatsSerializer(stats)
        return Response(
            {
                'message': 'Task statistics retrieved successfully',
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )