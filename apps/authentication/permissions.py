"""
Custom Permissions for Authentication
"""

from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permission to only allow admin users to access.
    """
    
    def has_permission(self, request, view):
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_admin or request.user.is_superuser)
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Permission to only allow owners of an object or admin to access it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Admin users have full access
        if request.user.is_admin or request.user.is_superuser:
            return True
        
        # Check if the object has a 'user' attribute
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # Check if the object is the user itself
        return obj == request.user


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Permission to allow unauthenticated users to create (register) 
    but require authentication for other operations.
    """
    
    def has_permission(self, request, view):
        # Allow POST requests (registration) without authentication
        if request.method == 'POST':
            return True
        
        # Require authentication for other methods
        return bool(request.user and request.user.is_authenticated)