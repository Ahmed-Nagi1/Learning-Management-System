from rest_framework.permissions import BasePermission

class IsInstructor(BasePermission):
    """
    Custom permission to allow access only to users with role 'instructor'.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated and has a role of 'instructor'
        return request.user.is_authenticated and request.user.role == 'instructor'
    
class IsAdmin(BasePermission):
    """
    Custom permission to allow access only to users with role 'instructor'.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated and has a role of 'instructor'
        return request.user.is_authenticated and request.user.role == 'admin'
