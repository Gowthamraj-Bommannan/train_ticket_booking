from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer
from .models import User, Role
import pytz
from .exceptions import (APIException, InvalidInput, EmailAlreadyExists, 
                         UsernameAlreadyExists, MobileNumberAlreadyExists)

class RegisterView(APIView):
    def post(self, request):
        try:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            data = serializer.data
            data.pop('password', None)
            return Response({'message': 'User registered successfully.', 'user': data}, status=status.HTTP_201_CREATED)
        except (InvalidInput, EmailAlreadyExists, UsernameAlreadyExists, MobileNumberAlreadyExists) as e:
            return Response({'success': False, 'message': e.detail}, status=e.status_code)
        except APIException as e:
            return Response({'success': False, 'error': str(e)}, status=e.status_code)
        except Exception as e:
            return Response({'success': False, 'error': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
