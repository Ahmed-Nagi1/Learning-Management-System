from rest_framework import serializers
from .models import *
from dj_rest_auth.serializers import LoginSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from allauth.account.models import EmailAddress
from dj_rest_auth.registration.serializers import RegisterSerializer



class CustomLoginSerializer(LoginSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Please enter both email and password.")

        User = get_user_model()
        users = User.objects.filter(email=email)

        if not users.exists():
            raise serializers.ValidationError("Incorrect email.")

        if users.count() > 1:
            raise serializers.ValidationError("Multiple users found with this email. Please contact support.")

        user = users.first()

        if not user.check_password(password):
            raise serializers.ValidationError("Incorrect password.")

        if not self.is_email_verified(user):
            raise serializers.ValidationError("Email not verified. Please verify your email first.")

        attrs['user'] = user
        return attrs


    def is_email_verified(self, user):
        if hasattr(user, 'email_verified'):
            return user.email_verified
        else:
            try:
                email_address = EmailAddress.objects.get(user=user, email=user.email)
                return email_address.verified
            except EmailAddress.DoesNotExist:
                return False




class CustomRegisterSerializer(RegisterSerializer):
    full_name = serializers.CharField(required=True)

    def save(self, request):
        user = super().save(request)
        user.full_name = self.data.get('full_name', '')
        user.save()
        return user

























class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()



