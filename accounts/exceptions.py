from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from utils.constants import AlreadyExistsMessage, UserMessage, GeneralMessage


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, (EmailAlreadyExists, UsernameAlreadyExists, 
                        MobileNumberAlreadyExists,InvalidCredentials)):
        return Response({'success': 'False',
                         'error': exc.default_detail,
                         'status': exc.status_code},
                         status=exc.status_code)
    
    elif isinstance(exc, (AlreadyExists, NotFound, InvalidInput)):
            # Show the exact message passed to InvalidInput
            response.data = {
                'success': False,
                'error': str(exc.detail)
            }

    if response is not None:
        response.data['success'] = False
        return response
    
    return Response({'success': False, 
                     'error': 'An unexpected error occurred.',
                     'detail':str(exc)
                     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = AlreadyExistsMessage.EMAIL_ALREADY_EXISTS
    default_code = 'email_exists'

class UsernameAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = AlreadyExistsMessage.USERNAME_ALREADY_EXISTS
    default_code = 'username_exists'

class MobileNumberAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = AlreadyExistsMessage.MOBILE_ALREADY_EXISTS
    default_code = 'mobile_number_exists'

class InvalidCredentials(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = UserMessage.INVALID_CREDENTIALS
    default_code = 'invalid_credentials'

class AlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'already_exists'

class InvalidInput(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid_input'

class QueryParameterMissing(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = GeneralMessage.QUERY_MISSING
    default_code = 'missing_query'


class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'not_found'
