import logging
import datetime

logger = logging.getLogger('request_logger')

class LoggingMiddleware:
    """
    Middleware to log request and response details.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log request details
        logger.info(f"Request: {request.method} {request.get_full_path()} at {datetime.datetime.now()}")
        
        response = self.get_response(request)
        
        # Log response details
        logger.info(f"Response: {response.status_code} at {datetime.datetime.now()}")
        
        return response