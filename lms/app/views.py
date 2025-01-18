from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from .permissions import IsOwnerOrReadOnly, IsAdmin
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied


class CourseViewSet(ModelViewSet):
    """
    A ViewSet for viewing and editing Course instances.
    """
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CourseSerializer

    def perform_create(self, serializer):
        """
        Save the post data when creating a new course.
        """
        serializer.save(owner=self.request.user)
        
    @action(detail=False, methods=['get'], url_path='my-courses', url_name='my_courses')
    def get_my_course(self, request):
        """
        Custom GET method to fetch detailed information about my courses.
        """
        
        my_courses = Course.objects.filter(owner=request.user)
    
        # Serialize the data
        serializer = self.get_serializer(my_courses, many=True)
        
        return Response(serializer.data)



class ModuleViewSet(ModelViewSet):
    """
    ViewSet for managing modules.
    """

    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]    

    def get_queryset(self):
        """
        Return modules only if the user is the course owner.
        """
        course_id = self.request.query_params.get('pk')  
        if course_id:
            course = Course.objects.filter(id=course_id).first()
            if course:
                return Module.objects.filter(course=course)
        return Module.objects.none()


    def perform_create(self, serializer):
        """
        Allow only the course owner to create a module.
        """
        course_id = self.request.data.get('course')
        course = Course.objects.filter(id=course_id, owner=self.request.user).first()
        is_owner = course.owner == self.request.user
        if not is_owner:
            raise PermissionDenied("You do not have permission to create module.")
        
        if not course:
            return Response(
                {"detail": "This course not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer.save(course=course, created_by=self.request.user)
        


class LessonViewSet(ModelViewSet):
    """
    ViewSet for managing lessons.
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]    

    def get_queryset(self):
        """
        Return a specific lesson within a specific module only if the user is authorized.
        """

        lesson_id = self.request.query_params.get('lesson_id')  # Get lesson ID from the request
        module_id = self.request.query_params.get('module_id')  # Get module ID from the request

        # Check if both lesson_id and module_id are provided
        if not lesson_id or not module_id:
            return Lesson.objects.none()  # Return no results if either is missing

        # Verify that the module exist  
        module = Module.objects.filter(id=module_id).first()
        if not module:
            return Lesson.objects.none()  # Return no results if the module does not exist

        # Verify that the lesson exists and is associated with the module
        lesson = Lesson.objects.filter(id=lesson_id, module=module).first()
        if not lesson:
            return Lesson.objects.none()  # Return no results if the lesson does not exist or is not linked to the module

        # Check if the user has access (owner of the course or enrolled in the course)
        is_owner = module.course.owner == self.request.user
        is_enrolled = Enrollment.objects.filter(course=module.course, student=self.request.user).exists()

        if is_owner or is_enrolled:
            
            return Lesson.objects.filter(id=lesson_id) # Return the lesson if the user is authorized

        return Lesson.objects.none()  # Deny access if the user is not authorized
        
    def perform_create(self, serializer):
        """
        Customize the creation of a lesson to include the module and the user who created it.
        """
        module_id = self.request.data.get('module')  # Get the module ID from the request
        module = Module.objects.filter(id=module_id).first()  # Fetch the module
        is_owner = module.course.owner == self.request.user
        if not is_owner:
            raise PermissionDenied("You do not have permission to create lessons in this module.")

        if not module:
            raise serializers.ValidationError({"module": "Module does not exist."})

        # Save the lesson with the module and created_by user
        serializer.save(module=module, created_by=self.request.user)

    @action(detail=False, methods=['patch'], url_path='update-lesson')
    def patch_lesson(self, request, *args, **kwargs):
        """
        Custom PATCH method to update a lesson.
        """
        # الحصول على معرف الكائن (lesson_id) من الـ URL
        lesson_id = self.request.query_params.get('lesson_id')
        if not lesson_id:
            return Response({"detail": "Lesson ID is required in the URL."}, status=status.HTTP_400_BAD_REQUEST)

        # البحث عن الدرس
        lesson = Lesson.objects.filter(id=lesson_id).first()
        if not lesson:
            return Response({"detail": "Lesson not found."}, status=status.HTTP_404_NOT_FOUND)

        # التحقق من الصلاحيات (مالك الكورس أو مسجل فيه)
        is_owner = lesson.module.course.owner == request.user

        if not is_owner:
            raise PermissionDenied("You do not have permission to update this lesson.")

        # تحديث الدرس باستخدام البيانات المرسلة في الطلب
        serializer = self.get_serializer(lesson, data=request.data, partial=True)  # partial=True لتحديث الحقول المطلوبة فقط
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    
    @action(detail=False, methods=['delete'], url_path='delete-lesson')
    def delete_lesson(self, request, *args, **kwargs):
        """
        Custom DELETE method to delete a lesson.
        """
        # الحصول على معرف الكائن (lesson_id) من الـ URL
        lesson_id = request.query_params.get('lesson_id')
        if not lesson_id:
            return Response(
                {"detail": "Lesson ID is required in the URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # البحث عن الدرس
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {"detail": "Lesson not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # التحقق من الصلاحيات (مالك الكورس أو مسجل فيه)
        is_owner = lesson.module.course.owner == request.user

        if not is_owner:
            raise PermissionDenied("You do not have permission to delete this lesson.")

        # حذف الدرس
        lesson.delete()

        return Response(
            {"detail": "Lesson deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )



class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete']
    
    def list(self, request, *args, **kwargs):
        instance = Enrollment.objects.filter(student=request.user)
        
        serializer = self.get_serializer(instance, many=True)
        return Response(serializer.data) 


    def create(self, request, *args, **kwargs):
        
        course_id = request.data.get('course_id')

        # Check if the student and course exist
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        if Enrollment.objects.filter(student=request.user, course=course).exists():
            return Response({"detail": "You are already subscribed to this course."}, status=status.HTTP_404_NOT_FOUND)
        elif course.owner == request.user:
            return Response({"detail": "You can't enroll in your course"}, status=status.HTTP_404_NOT_FOUND)
        
        # Create a new enrollment
        enrollment = Enrollment.objects.create(student=request.user, course=course)
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    
class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        
        # Ensure the user is an owner
        if request.user.role != 'owner':
            return Response({"detail": "Only owners can create quizzes"}, status=status.HTTP_403_FORBIDDEN)
        # Get course data from the request
        moduleId = request.data.get('module')
        # Check if the course exists
        try:
            module = Module.objects.get(id=moduleId)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        # Ensure the current owner is the course owner
        if module.course.owner != request.user:
            return Response({"detail": "You can only create quizzes for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        # Create a new quiz
        quiz = Quiz.objects.create(module=module)
        serializer = self.get_serializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, *args, **kwargs):
        # Ensure the user is an owner
        if request.user.role != 'owner':
            return Response({"detail": "Only owners can update quizzes"}, status=status.HTTP_403_FORBIDDEN)
        # Get the quiz object to update
        quiz = self.get_object()
        # Ensure the current owner is the course owner
        if quiz.module.course.owner != request.user:
            return Response({"detail": "You can only update quizzes for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        # Update the quiz
        serializer = self.get_serializer(quiz, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        
        # Ensure the user is an owner
        if request.user.role != 'owner':
            return Response({"detail": "Only owners can delete quizzes"}, status=status.HTTP_403_FORBIDDEN)
        # Get the quiz object to delete
        quiz = self.get_object()
        # Ensure the current owner is the course owner
        if quiz.module.course.owner != request.user:
            return Response({"detail": "You can only delete quizzes for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        # Delete the quiz
        quiz.delete()
        return Response({"detail": "Quiz deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
   
    
# class CertificateViewSet(ModelViewSet):
#     queryset = Certificate.objects.all()
#     serializer_class = CertificateSerializer
#     permission_classes = []
    
#     def get_permissions(self):
#         if self.action == 'create':
#             # permission_classes = [Isowner]
#             pass
#         elif self.action in ['update', 'destroy']:
#             permission_classes = [IsAdmin]
#         # else:
#         #     permission_classes = []  
#         # return [permission() for permission in permission_classes]
        
        
#     def create(self, request, *args, **kwargs):
        
#         # Get course data from the request
#         courseId = request.data.get('course')
#         student_id = request.data.get('student')
#         # Check if the course exists
#         try:
#             course = Course.objects.get(id=courseId)
#             student = User.objects.get(id=student_id, role='student')
#         except User.DoesNotExist:
#             return Response({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
#         except Course.DoesNotExist:
#             return Response({"detail": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
#         # Ensure the current owner is the course owner
#         if course.owner != request.user:
#             return Response({"detail": "You can only create certificate for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        
#         certificate = Certificate.objects.create(course=course, student=student)
#         serializer = self.get_serializer(certificate)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    