from rest_framework.permissions import IsAuthenticated, BasePermission, SAFE_METHODS 
import logging

logger = logging.getLogger(__name__)

class IsOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):
      
        if request.method in SAFE_METHODS:
            return True
        
        view_name = view.__class__.__name__
        match view_name:
            case "CourseViewSet":
                return obj.owner == request.user
                
            case "ModuleViewSet":
                return obj.created_by == request.user
                
            case "LessonViewSet":
                return obj.created_by == request.user
            
            case "EnrollmentViewSet":
                return obj.student == request.user
                

  
  
class IsAdmin(BasePermission):
    """
    Custom permission to allow access only to users with role 'instructor'.
    """

    def has_permission(self, request, view):
        # Ensure the user is authenticated and has a role of 'instructor'
        return request.user.is_authenticated and request.user.role == 'admin'
