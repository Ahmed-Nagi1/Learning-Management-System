from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework.permissions import AllowAny
from .serializers import ChangeEmailSerializer


class CustomConfirmEmailView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ChangeEmailSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_email = serializer.validated_data['email']

            # تغيير البريد الإلكتروني
            email_address, created = EmailAddress.objects.get_or_create(user=user, email=new_email)
            if not email_address.verified:
                send_email_confirmation(request, user, email=email_address.email)

            return Response({"message": "تم إرسال بريد تأكيد إلى البريد الإلكتروني الجديد."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)