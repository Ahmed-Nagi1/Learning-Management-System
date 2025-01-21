from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    image = models.ImageField(upload_to="courses/image", null=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', verbose_name="Owner")      
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def str(self):
        return self.title
    
    def clean(self):
        if self.is_paid and (self.price is None or self.price <= 0):
            raise ValidationError({'price': 'Price must be set and greater than 0 for paid products.'})  
        
        if not self.is_paid and self.price:
            raise ValidationError({'price': 'Price must be empty for free products.'})


class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Module Title")
    description = models.TextField(null=True, verbose_name="Module Description")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name="Course")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Created By")

    def str(self):
        return self.title

class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Lesson Title")
    description = models.TextField(null=True, verbose_name="Lesson Description")
    content = models.TextField(verbose_name="Lesson Content")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name="Module")
    file = models.FileField(upload_to='lesson_files/', null=True, blank=True, verbose_name="Attached File")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Created By")
    quiz = models.JSONField(null=True)

    def str(self):
        return self.title

class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students_enrollments', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Course")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Enrollment Date")
    completed = models.BooleanField(default=False, verbose_name="Completed")

    def str(self):
        return f"{self.student.username} - {self.course.title}"

class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates', verbose_name="Course")
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="Issued At")
    certificate_file = models.FileField(upload_to='certificates/', verbose_name="Certificate File")

    def str(self):
        return f"{self.student.username} - {self.course.title}"





class AD(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='ads_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title