from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ChangeEmailSerializer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from lms.utils.exception_handler import CustomValidationError
User = get_user_model()

class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user 
        image_url = request.build_absolute_uri(user.image.url) if user.image else None
        return Response({
            "name": user.full_name,
            "image": image_url
        })

    def patch(self, request):
        print(request.data)
        user = request.user
        full_name = request.data.get('full_name')

        if full_name:
            user.full_name = full_name

        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user.image = profile_image
            print("Ok")
        user.save()

        return Response(
            {"ok"},
            status=status.HTTP_200_OK
        )
                


class ChangeEmailView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Confirmation email has been sent to the new address.",
                }, status=status.HTTP_200_OK)
        
        raise CustomValidationError(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ConfirmEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        key = request.data.get("key")
        if not key:
            raise CustomValidationError({"detail": _("Key is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to retrieve the email confirmation using HMAC key
            email_confirmation = EmailConfirmationHMAC.from_key(key)
            if email_confirmation is None:
                # If HMAC fails, fallback to database key
                email_confirmation = EmailConfirmation.objects.get(key=key)
        except EmailConfirmation.DoesNotExist:
            raise CustomValidationError({"detail": _("Invalid or expired key.")}, status=status.HTTP_400_BAD_REQUEST)

        if email_confirmation.email_address.verified:
            return Response({"detail": _("Email is already verified.")}, status=status.HTTP_200_OK)

        # Verify the email
        email_confirmation.confirm(request)
        email = email_confirmation.email_address.email
        return Response({"detail": _("Email successfully verified."), "email": email}, status=status.HTTP_200_OK)
