from rest_framework.exceptions import APIException
from rest_framework import status

class EmailAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Email already exists.'
    default_code = 'email_exists'

class UsernameAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Username already exists.'
    default_code = 'username_exists'

class MobileNumberAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Mobile number already exists.'
    default_code = 'mobile_number_exists'

class InvalidCredentials(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Invalid username or password.'
    default_code = 'invalid_credentials'

class InvalidInput(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid input.'
    default_code = 'invalid_input'
