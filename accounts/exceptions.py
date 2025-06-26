from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, (EmailAlreadyExists, UsernameAlreadyExists, 
                        MobileNumberAlreadyExists,InvalidCredentials)):
        return Response({'success': 'False',
                         'error': exc.default_detail,
                         'status': exc.status_code},
                         status=exc.status_code)
    
    elif isinstance(exc, InvalidInput):
            # Show the exact message passed to InvalidInput
            response.data = {
                'success': False,
                'error': str(exc.detail)
            }

    if response is not None:
        response.data['success'] = False
        return response
    
    return Response({'success': False, 
                     'error': 'An unexpected error occurred.'
                     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
    # default_detail = 'Invalid input.'
    default_code = 'invalid_input'
