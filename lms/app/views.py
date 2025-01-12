from django.shortcuts import render
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, BasePermission
from .permissions import IsInstructor, IsAdmin




class CourseRead(ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()



class CourseViewSet(ModelViewSet):
    """
    A ViewSet for viewing and editing Course instances.
    """
    permission_classes = [IsAuthenticated,]
    serializer_class = CourseSerializer
    
    def get_queryset(self):
        """
        Return courses belonging to the authenticated user.
        """
        user = self.request.user
        return Course.objects.filter(instructor=user)

    def perform_create(self, serializer):
        """
        Save the post data when creating a new course.
        """
        user = self.request.user


        serializer.save(instructor=user)

    def perform_update(self, serializer):
        """
        Ensure that only the instructor can update their course.
        """
        course = self.get_object()
        if course.instructor != self.request.user:
            return Response(
                {"detail": "You do not have permission to edit this course."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()

    def perform_destroy(self, instance):
        """
        Ensure that only the instructor can delete their course.
        """
        if instance.instructor != self.request.user:
            return Response(
                {"detail": "You do not have permission to delete this course."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()









class ModuleViewSet(ModelViewSet):
    """
    ViewSet for managing modules.
    """

    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    

    def get_queryset(self):
        """
        Return modules only if the user is the course instructor.
        """
        course_id = self.request.query_params.get('course_id')  
        if course_id:
            course = Course.objects.filter(id=course_id).first()
            if course:
                return Module.objects.filter(course=course).order_by('order')
        return Module.objects.none()


    def perform_create(self, serializer):
        """
        Allow only the course instructor to create a module.
        """
        course_id = self.request.data.get('course')
        course = Course.objects.filter(id=course_id, instructor=self.request.user).first()
        if not course:
            return Response(
                {"detail": "You do not have permission to delete this course."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save(course=course)

    def perform_update(self, serializer):
        """
        Allow only the course instructor to update the module.
        """
        module = self.get_object()
        if module.course.instructor != self.request.user:
            return Response(
                {"detail": "You do not have permission to delete this course."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()

    def perform_destroy(self, instance):
        """
        Allow only the course instructor to delete the module.
        """
        if instance.course.instructor != self.request.user:
            return Response(
                {"detail": "You do not have permission to delete this course."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()

class LessonViewSet(ModelViewSet):
    """
    ViewSet for managing lessons.
    """

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    

    def get_queryset(self):
        """
        Return lessons only if the user is authorized (instructor or student) and provides valid data.
        """
        # حالة جلب كائن واحد
        if self.kwargs.get(self.lookup_field):  # 'id' by default
            lesson = Lesson.objects.filter(id=self.kwargs[self.lookup_field]).first()
            if lesson:
                course = lesson.module.course
                # التحقق من الصلاحيات
                if course.instructor == self.request.user or Enrollment.objects.filter(student=self.request.user, course=course).exists():
                    return Lesson.objects.filter(id=lesson.id)
            return Lesson.objects.none()

        # حالة جلب مجموعة بناءً على module_id
        module_id = self.request.query_params.get('module_id')
        if module_id:
            module = Module.objects.filter(id=module_id).first()
            if module:
                course = module.course
                # التحقق من الصلاحيات
                if course.instructor == self.request.user or Enrollment.objects.filter(student=self.request.user, course=course).exists():
                    queryset = Lesson.objects.filter(module=module).order_by('order')
                    print(f"Queryset: {queryset}")
                    return queryset

        # في حالة عدم وجود صلاحيات أو عدم تطابق البيانات
        return Lesson.objects.none()


    def perform_create(self, serializer):
        """
        Allow only the course instructor to create a lesson within their module.
        """
        module_id = self.request.data.get('module')
        module = Module.objects.filter(id=module_id, course__instructor=self.request.user).first()
        if not module:
            return Response(
                {"detail": "You do not have permission to create a lesson in this module."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save(module=module)
        

    def perform_update(self, serializer):
        """
        Allow only the course instructor to update a lesson within their module.
        """
        lesson = self.get_object()
        if lesson.module.course.instructor != self.request.user:
            return Response(
                {"detail": "You do not have permission to update this lesson."},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()

    def perform_destroy(self, instance):
        """
        Allow only the course instructor to delete a lesson within their module.
        """
        
        if instance.module.course.instructor != self.request.user:
            return Response(
                {"detail": "You do not have permission to delete this lesson."},
                status=status.HTTP_403_FORBIDDEN,
            )
        instance.delete()

class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Ensure the user is an instructor
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can enroll students"}, status=status.HTTP_403_FORBIDDEN)

        # Get student and course data from the request
        student_id = request.data.get('student_id')
        course_id = request.data.get('course_id')

        # Check if the student and course exist
        try:
            student = User.objects.get(id=student_id, role='student')
            course = Course.objects.get(id=course_id)
        except User.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure the current instructor is the course instructor
        if course.instructor != request.user:
            return Response({"error": "You can only enroll students in your own courses"}, status=status.HTTP_403_FORBIDDEN)

        # Create a new enrollment
        enrollment = Enrollment.objects.create(student=student, course=course)
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        # Ensure the user is an instructor
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can update enrollments"}, status=status.HTTP_403_FORBIDDEN)

        # Get the enrollment object to update
        enrollment = self.get_object()

        # Ensure the current instructor is the course instructor
        if enrollment.course.instructor != request.user:
            return Response({"error": "You can only update enrollments in your own courses"}, status=status.HTTP_403_FORBIDDEN)

        # Update the enrollment
        serializer = self.get_serializer(enrollment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        # Ensure the user is an instructor
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can delete enrollments"}, status=status.HTTP_403_FORBIDDEN)

        # Get the enrollment object to delete
        enrollment = self.get_object()

        # Ensure the current instructor is the course instructor
        if enrollment.course.instructor != request.user:
            return Response({"error": "You can only delete enrollments in your own courses"}, status=status.HTTP_403_FORBIDDEN)

        # Delete the enrollment
        enrollment.delete()
        return Response({"message": "Enrollment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        
        # Ensure the user is an instructor
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can create quizzes"}, status=status.HTTP_403_FORBIDDEN)
        # Get course data from the request
        moduleId = request.data.get('module')
        # Check if the course exists
        try:
            module = Module.objects.get(id=moduleId)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        # Ensure the current instructor is the course instructor
        if module.course.instructor != request.user:
            return Response({"error": "You can only create quizzes for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        # Create a new quiz
        # data = request.data.copy()  # نسخ البيانات لتجنب التعديل على الأصل
        # data.pop('module', None)  # إزالة المفتاح module إذا كان موجودًا
        quiz = Quiz.objects.create(module=module)
        serializer = self.get_serializer(quiz)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
    def update(self, request, *args, **kwargs):
        # Ensure the user is an instructor
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can update quizzes"}, status=status.HTTP_403_FORBIDDEN)
        # Get the quiz object to update
        quiz = self.get_object()
        # Ensure the current instructor is the course instructor
        if quiz.module.course.instructor != request.user:
            return Response({"error": "You can only update quizzes for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        # Update the quiz
        serializer = self.get_serializer(quiz, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, *args, **kwargs):
        
        # Ensure the user is an instructor
        if request.user.role != 'instructor':
            return Response({"error": "Only instructors can delete quizzes"}, status=status.HTTP_403_FORBIDDEN)
        # Get the quiz object to delete
        quiz = self.get_object()
        # Ensure the current instructor is the course instructor
        if quiz.module.course.instructor != request.user:
            return Response({"error": "You can only delete quizzes for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        # Delete the quiz
        quiz.delete()
        return Response({"message": "Quiz deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
   
    
class CertificateViewSet(ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = []
    
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsInstructor]
        elif self.action in ['update', 'destroy']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = []  
        return [permission() for permission in permission_classes]
        
        
    def create(self, request, *args, **kwargs):
        
        # Get course data from the request
        courseId = request.data.get('course')
        student_id = request.data.get('student')
        # Check if the course exists
        try:
            course = Course.objects.get(id=courseId)
            student = User.objects.get(id=student_id, role='student')
        except User.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        # Ensure the current instructor is the course instructor
        if course.instructor != request.user:
            return Response({"error": "You can only create certificate for your own courses"}, status=status.HTTP_403_FORBIDDEN)
        
        certificate = Certificate.objects.create(course=course, student=student)
        serializer = self.get_serializer(certificate)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    