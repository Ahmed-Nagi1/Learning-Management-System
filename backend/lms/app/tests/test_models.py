from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from lms.app.models import Course, Module, Lesson, Enrollment, Certificate, AD
from uuid import uuid4

User = get_user_model()


class ModelsTestCase(TestCase):

    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(email='testuser@email.com', password='password')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # Create a test course
        self.course = Course.objects.create(
            title="Test Course",
            description="A test course description",
            is_paid=True,
            price=100.00,
            owner=self.user
        )

    def test_course_creation(self):
        """Test creating a course"""
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.title, "Test Course")
        self.assertTrue(self.course.is_paid)
        self.assertEqual(self.course.price, 100.00)

    def test_course_validation(self):
        """Test course validation logic"""
        course = Course(
            title="Invalid Course",
            description="Should fail validation",
            is_paid=True,
            price=None,  # Invalid case
            owner=self.user
        )
        with self.assertRaises(ValidationError):
            course.clean()

    def test_module_creation(self):
        """Test creating a module"""
        module = Module.objects.create(
            title="Test Module",
            description="A test module description",
            course=self.course,
            created_by=self.user
        )
        self.assertEqual(Module.objects.count(), 1)
        self.assertEqual(module.title, "Test Module")

    def test_lesson_creation(self):
        """Test creating a lesson"""
        module = Module.objects.create(
            title="Test Module",
            course=self.course,
            created_by=self.user
        )
        lesson = Lesson.objects.create(
            title="Test Lesson",
            description="A test lesson description",
            content="Lesson content here",
            module=module,
            created_by=self.user
        )
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(lesson.title, "Test Lesson")
        self.assertEqual(lesson.module, module)

    def test_enrollment_creation(self):
        """Test creating an enrollment"""
        enrollment = Enrollment.objects.create(
            student=self.user,
            course=self.course,
            completed=False
        )
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(enrollment.student, self.user)
        self.assertEqual(enrollment.course, self.course)

    def test_certificate_creation(self):
        """Test creating a certificate"""
        certificate = Certificate.objects.create(
            student=self.user,
            course=self.course,
            certificate_file='path/to/certificate.pdf'
        )
        self.assertEqual(Certificate.objects.count(), 1)
        self.assertEqual(certificate.student, self.user)
        self.assertEqual(certificate.course, self.course)

    def test_ad_creation(self):
        """Test creating an ad"""
        ad = AD.objects.create(
            title="Test Ad",
            description="This is a test ad",
            image=None
        )
        self.assertEqual(AD.objects.count(), 1)
        self.assertEqual(ad.title, "Test Ad")
        self.assertEqual(ad.description, "This is a test ad")
