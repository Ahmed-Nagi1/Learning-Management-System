from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework import status


class CustomSuccessResponse(Response):
    def __init__(self, detail=None, code=status.HTTP_200_OK):
        data = {"success": True}
        if detail is not None:
            data["detail"] = detail
        super().__init__(data, status=code)



class CustomValidationError(APIException):
    status_code = 400
    default_detail = 'A validation error occurred.'
    default_code = 'validation_error'

    def __init__(self, detail=None, code=None):
        if detail is not None:
            self.detail = detail
        if code is not None:
            self.status_code = code
