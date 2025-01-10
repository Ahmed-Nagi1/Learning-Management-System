from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    role = {
        ('student', 'student'),
        ('instructor', 'instructor'),
        ('admin', 'admin'),
    }
    first_name = None  
    last_name = None   
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, null=True) 
    role = models.CharField(max_length=255, null=True, choices=role)

    
    def __str__(self):
        return self.email
