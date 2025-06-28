from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if isinstance(exc, ()):
        return Response({'success': 'False',
                         'error': str(exc.detail),
                         'status': exc.status_code},
                         status=exc.status_code)
    
    elif isinstance(exc, (InvalidInput, AlreadyExists)):
            # Show the exact message passed to InvalidInput
            response.data = {
                'success': False,
                'error': str(exc.detail)
            }

    if response is not None:
        response.data['success'] = False
        return response
    
    # print(response)
    
    return Response({'success': False, 
                     'error': str(exc)
                     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoesNotExists(APIException):
     """
    Generic exception used when a resource is not found.
    
    Arguments:
        detail (str): Custom message like 'Station not found.'
    Returns:
        404 HTTP response with JSON error.
    """
     status_code = status.HTTP_404_NOT_FOUND
     default_code = 'not_found'

     def __init__(self, detail=None):
        if detail is None:
            detail = "Resource not found."
        self.detail = {'error': detail}

class QueryParameterMissing(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Search query parameter is required.'
    default_code = 'missing_query'

class InvalidInput(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'invalid_input'

class AlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = 'already_exists'