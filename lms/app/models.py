from django.db import models
from uuid import uuid4
from django.contrib.auth import get_user_model


User = get_user_model()

# Table for courses (Course)
class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Course Title")
    description = models.TextField(verbose_name="Course Description")
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught', verbose_name="Instructor")           
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def str(self):
        return self.title

# Table for modules (Module)
class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Module Title")
    description = models.TextField(verbose_name="Module Description")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', verbose_name="Course")
    order = models.PositiveIntegerField(default=0, verbose_name="Order", unique=True)

    def str(self):
        return self.title

# Table for lessons (Lesson)
class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Lesson Title")
    content = models.TextField(verbose_name="Lesson Content")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='lessons', verbose_name="Module")
    order = models.PositiveIntegerField(default=0, verbose_name="Order")
    file = models.FileField(upload_to='lesson_files/', null=True, blank=True, verbose_name="Attached File")

    def str(self):
        return self.title

# Table for enrollments (Enrollment)
class Enrollment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', verbose_name="Course")
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Enrollment Date")
    completed = models.BooleanField(default=False, verbose_name="Completed")

    def str(self):
        return f"{self.student.username} - {self.course.title}"

# Table for quizzes (Quiz)
class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, verbose_name="Quiz Title")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='quiz', verbose_name="Module")
    questions = models.JSONField(verbose_name="Questions", null=True)  # Stores questions as a JSON list

    def str(self):
        return self.title


    def str(self):
        return f"{self.student.username} - {self.quiz.title}"

# Table for certificates (Certificate)
class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='certificates', verbose_name="Student")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates', verbose_name="Course")
    issued_at = models.DateTimeField(auto_now_add=True, verbose_name="Issued At")
    certificate_file = models.FileField(upload_to='certificates/', verbose_name="Certificate File")

    def str(self):
        return f"{self.student.username} - {self.course.title}"
