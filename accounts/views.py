from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer
import logging

logger = logging.getLogger('request_logger')

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        data.pop('password', None)
        logger.info(f"User registered successfully. {user.username}")
        return Response({'message': 'User registered successfully.', 'user': data}, status=status.HTTP_201_CREATED)
