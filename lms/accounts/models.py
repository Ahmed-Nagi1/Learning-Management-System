from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    # إزالة الحقل username من AbstractUser
    username = None  
    first_name = None  
    last_name = None  

    # الحقول الخاصة بالمستخدم المخصص
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    # تخصيص مدير المستخدم
    objects = CustomUserManager()

    # تحديد الحقول الأساسية
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # قائمة الحقول المطلوبة لإنشاء مستخدم عبر createsuperuser

    def __str__(self):
        return self.email
