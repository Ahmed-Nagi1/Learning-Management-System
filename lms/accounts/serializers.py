from rest_framework import serializers
from .models import *
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from allauth.account.utils import send_email_confirmation
from rest_framework.response import Response
from lms.utils.exception_handler import CustomValidationError


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class CustomLoginSerializer(LoginSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise CustomValidationError(_("Please enter both email and password."))

        # البحث عن المستخدم بالبريد الإلكتروني
        users = User.objects.filter(email=email)
        email_address = EmailAddress.objects.filter(email=email).first()

        if not users.exists():
            raise CustomValidationError(_("No account found with this email."))
        
        if not email_address.verified: 
            CustomValidationError(_("Email not verified. Please verify your email first."))

        if users.count() > 1:
            raise CustomValidationError(_("Multiple accounts found with this email. Please contact support."))

        user = users.first()

        if not user.check_password(password):
            raise CustomValidationError(_("Incorrect password."))

        if not self.is_email_verified(user):
            raise CustomValidationError(_("Email not verified. Please verify your email first."))

        # إضافة المستخدم إلى الـ attrs
        attrs['user'] = user
        return attrs

    def is_email_verified(self, user):
        """
        التحقق من حالة التحقق من البريد الإلكتروني.
        """
        try:
            # استخدام نموذج EmailAddress للتحقق
            email_address = EmailAddress.objects.get(user=user, email=user.email)
            return email_address.verified
        except EmailAddress.DoesNotExist:
            return False


class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(required=True)

    def save(self, request):
        email = self.data.get('email')

        email_address = EmailAddress.objects.filter(email=email).first()
        if email_address:
            if email_address.verified: 
                raise CustomValidationError({'email': 'This email is already.'})
            else: 
                send_email_confirmation(request, email_address.user)
                raise CustomValidationError({'email': 'A confirmation email has been sent. Please confirm your email.'})
        
        user = super().save(request)
        user.full_name = self.data.get('full_name', '')
        user.save()
       
        send_email_confirmation(request, user)
        return user






class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if EmailAddress.objects.filter(email=value).exists() or User.objects.filter(email=value).exists():
            raise CustomValidationError("This email is already in use.")
        return value

    def save(self, user):
        email = self.validated_data["email"]
        EmailAddress.objects.filter(user=user, verified=False).delete() # حذف الايميلات السابقة
        
        email_address, created = EmailAddress.objects.get_or_create(
            user=user,
            email=email,
            defaults={"primary": False, "verified": False}
        )
        
        if created:
            send_email_confirmation(self.context["request"], user, email=email)
            
        return email