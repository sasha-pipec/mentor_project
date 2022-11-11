from rest_framework import status
from rest_framework.exceptions import APIException


class ValidationError401(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED

class ValidationError409(APIException):
    status_code = status.HTTP_409_CONFLICT

class ValidationError400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST

class ValidationError404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
