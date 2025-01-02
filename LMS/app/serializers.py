from rest_framework import serializers
from .models import *


class CourseSerializer(serializers.HyperlinkedModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    class Meta:
        model = Course
        fields = ['url', 'id', 'title', 'description', 'instructor_name', 'created_at', 'updated_at']

class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Module
        fields = ['url', 'id', 'title', 'description', 'course', 'order']
        extra_kwargs = {
            'url': {'view_name': 'modules-detail', 'lookup_field': 'id'}
        }


class LessonSerializer(serializers.HyperlinkedModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())

    class Meta:
        model = Lesson
        fields = ['url', 'id', 'title', 'content', 'module', 'order', 'file']
        extra_kwargs = {
            'url': {'view_name': 'lessons-detail', 'lookup_field': 'id'}
        }


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'student', 'course', 'enrolled_at', 'completed']
        
        
class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'module', 'questions']