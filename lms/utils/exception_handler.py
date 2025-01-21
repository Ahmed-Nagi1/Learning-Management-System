from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


class CustomValidationError(APIException):
    default_status = status.HTTP_400_BAD_REQUEST
    default_detail = 'A validation error occurred.'

    def __init__(self, detail=None, status=None):
        self.detail = detail if detail is not None else self.default_detail
        self.status = status if status is not None else self.default_status

    def __str__(self):
        return f"{self.detail} (Status: {self.status})"

    @property
    def status_code(self):
        # Map `status` to `status_code` to ensure compatibility with DRF
        return self.status


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Handle CustomValidationError
    if isinstance(exc, CustomValidationError):
        return Response(
            {
                'error': exc.detail,
                'status_code': exc.status,
            },
            status=exc.status,
        )

    # Return the default response for other exceptions
    return response
