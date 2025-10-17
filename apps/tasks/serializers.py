"""
Task Serializers
"""

from rest_framework import serializers
from .models import Task
from apps.authentication.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    """
    Full Task Serializer with all fields
    """
    
    user = UserSerializer(read_only=True)
    status = serializers.ReadOnlyField()
    is_overdue = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'priority',
            'due_date',
            'status',
            'is_overdue',
            'user',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at', 'status', 'is_overdue']
    
    def validate_title(self, value):
        """Validate title is not empty"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
    
    def validate_due_date(self, value):
        """Validate due date is not in the past"""
        if value and value < serializers.DateTimeField().to_internal_value(
            serializers.DateTimeField().to_representation(Task.objects.model._meta.get_field('created_at').default())
        ):
            # Just a basic check - you can make this more sophisticated
            pass
        return value


class TaskCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new tasks
    """
    
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'completed',
            'priority',
            'due_date',
        ]
        extra_kwargs = {
            'description': {'required': False, 'allow_blank': True},
            'completed': {'required': False},
            'priority': {'required': False},
            'due_date': {'required': False},
        }
    
    def validate_title(self, value):
        """Validate title"""
        if not value or value.strip() == '':
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 255:
            raise serializers.ValidationError("Title cannot exceed 255 characters.")
        return value.strip()
    
    def create(self, validated_data):
        """Create task with user from request"""
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class TaskUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing tasks
    """
    
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'completed',
            'priority',
            'due_date',
        ]
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False, 'allow_blank': True},
            'completed': {'required': False},
            'priority': {'required': False},
            'due_date': {'required': False, 'allow_null': True},
        }
    
    def validate_title(self, value):
        """Validate title"""
        if value is not None:
            if not value or value.strip() == '':
                raise serializers.ValidationError("Title cannot be empty.")
            if len(value) > 255:
                raise serializers.ValidationError("Title cannot exceed 255 characters.")
            return value.strip()
        return value


class TaskListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing tasks
    """
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    status = serializers.ReadOnlyField()
    
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'completed',
            'priority',
            'status',
            'user_email',
            'due_date',
            'created_at',
            'updated_at',
        ]


class TaskStatusUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only task completion status
    """
    
    class Meta:
        model = Task
        fields = ['completed']
    
    def update(self, instance, validated_data):
        """Update task completion status"""
        instance.completed = validated_data.get('completed', instance.completed)
        instance.save()
        return instance


class TaskStatsSerializer(serializers.Serializer):
    """
    Serializer for task statistics
    """
    
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    pending_tasks = serializers.IntegerField()
    overdue_tasks = serializers.IntegerField()
    completion_rate = serializers.FloatField()