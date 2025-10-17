"""
Task Model
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class Task(models.Model):
    """
    Task Model with all required fields
    """
    
    # Required fields from specifications
    title = models.CharField(
        max_length=255,
        help_text="Title of the task"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the task"
    )
    completed = models.BooleanField(
        default=False,
        help_text="Task completion status"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when task was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when task was last updated"
    )
    
    # Additional field to associate task with user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks',
        help_text="User who owns this task"
    )
    
    # Optional fields for better task management
    priority = models.CharField(
        max_length=10,
        choices=[
            ('LOW', 'Low'),
            ('MEDIUM', 'Medium'),
            ('HIGH', 'High'),
        ],
        default='MEDIUM',
        help_text="Task priority level"
    )
    due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Due date for the task"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        indexes = [
            models.Index(fields=['user', 'completed']),
            models.Index(fields=['created_at']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    @property
    def is_overdue(self):
        """Check if task is overdue"""
        if self.due_date and not self.completed:
            return timezone.now() > self.due_date
        return False
    
    @property
    def status(self):
        """Get task status"""
        if self.completed:
            return "Completed"
        elif self.is_overdue:
            return "Overdue"
        else:
            return "Pending"
    
    def mark_as_completed(self):
        """Mark task as completed"""
        self.completed = True
        self.save()
    
    def mark_as_incomplete(self):
        """Mark task as incomplete"""
        self.completed = False
        self.save()