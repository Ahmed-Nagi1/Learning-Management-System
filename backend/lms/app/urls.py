from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'modules', ModuleViewSet, basename='modules')
router.register(r'lessons', LessonViewSet, basename='lessons')
router.register(r'enrollment', EnrollmentViewSet, basename='enrollment')
# router.register(r'certificate', CertificateViewSet, basename='certificate')

urlpatterns = [

] + router.urls