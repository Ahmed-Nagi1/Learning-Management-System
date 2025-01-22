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
    ROLE_CHOICES = {
        'student': 'Student',
        'instructor': 'Instructor',
        'admin': 'Admin',
    }
    username = None  
    first_name = None  
    last_name = None  

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="account/profile_image/", null=True, blank=True)

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email
