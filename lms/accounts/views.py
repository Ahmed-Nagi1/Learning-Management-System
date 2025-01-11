from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC, EmailAddress
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ChangeEmailSerializer
from asgiref.sync import sync_to_async

class ChangeEmailView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({
                "message": "Confirmation email has been sent to the new address.",
                }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class ConfirmEmailAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        key = request.data.get("key")
        if not key:
            return Response({"detail": _("Key is required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Attempt to retrieve the email confirmation using HMAC key
            email_confirmation = EmailConfirmationHMAC.from_key(key)
            if email_confirmation is None:
                # If HMAC fails, fallback to database key
                email_confirmation = EmailConfirmation.objects.get(key=key)
        except EmailConfirmation.DoesNotExist:
            return Response({"detail": _("Invalid or expired key.")}, status=status.HTTP_400_BAD_REQUEST)

        if email_confirmation.email_address.verified:
            return Response({"detail": _("Email is already verified.")}, status=status.HTTP_200_OK)

        # Verify the email
        email_confirmation.confirm(request)
        email = email_confirmation.email_address.email
        return Response({"detail": _("Email successfully verified."), "email": email}, status=status.HTTP_200_OK)
