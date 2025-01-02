from allauth.account.views import ConfirmEmailView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.permissions import AllowAny

class CustomConfirmEmailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        view = ConfirmEmailView.as_view()
        response = view(request, *args, **kwargs)
        if response.status_code == 302:  # Redirect on success
            return Response({"detail": "Email confirmed successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid confirmation link."}, status=status.HTTP_400_BAD_REQUEST)