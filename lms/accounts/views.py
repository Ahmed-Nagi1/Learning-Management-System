from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework.permissions import AllowAny
from .serializers import ChangeEmailSerializer


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

        return Response({"detail": _("Email successfully verified.")}, status=status.HTTP_200_OK)
