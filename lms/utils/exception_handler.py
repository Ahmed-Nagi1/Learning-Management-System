from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response


class CustomValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'A validation error occurred.'

    def __init__(self, detail=None, status=None):
        self.detail = detail if detail is not None else self.default_detail
        self.status = status if status is not None else self.status

    def __str__(self):
        return f"{self.detail} (Status: {self.status})"





def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    # Handle CustomValidationError
    if isinstance(exc, CustomValidationError):
        return Response(
            {
                'error': exc.detail,
                'status_code': exc.status_code,
            },
            status=exc.status_code,
        )

    # Return the default response for other exceptions
    return response