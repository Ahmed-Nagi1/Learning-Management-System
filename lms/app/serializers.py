from rest_framework import serializers
from .models import *
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer




class CourseSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.full_name', read_only=True)
    owner_image = serializers.SerializerMethodField()
    students_in_course = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'is_paid', 'price', 'image', 'owner_name', 'owner_image', 'students_in_course', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_owner_image(self, obj):
        request = self.context.get('request') 
        if obj.owner.image:
            return request.build_absolute_uri(obj.owner.image.url) 
        return None

    def get_students_in_course(self, obj):
        return Enrollment.objects.filter(course=obj).values('student').distinct().count()



class LessonSerializer(serializers.ModelSerializer):
    module = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all())

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'content', 'module', 'file']


class ModuleSerializer(serializers.ModelSerializer):
    lessons = serializers.SerializerMethodField()
    class Meta:
        model = Module
        fields = ['id', 'title', 'description', 'lessons', 'course']
        read_only_fields = ['course', 'lessons']
        
    def get_lessons(self, obj):
        return obj.lessons.values('id', 'title', 'description')



class EnrollmentSerializer(serializers.ModelSerializer):
    course_details = serializers.SerializerMethodField() 
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'course_details', 'enrolled_at', 'completed']
        read_only_fields = ['enrolled_at']
        
    def get_course_details(self, obj):
        course = obj.course
        request = self.context.get('request') 
        image_url = course.image.url if course.image else None
        
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)

        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "image": image_url,
            "is_paid": course.is_paid,
            "price": course.price,
            "rating": course.rating,
        }


        
class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = ['student', 'course', 'issued_at', 'certificate_file']


class PrivateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'student', 'enrolled_at']
        read_only_fields = ['enrolled_at']