from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from .models import User, Role
from django.contrib.auth.hashers import make_password
from utils.constants import UserMessage
import logging
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

logger = logging.getLogger('request_logger')

class RegisterView(APIView):
    """
    API endpoint for user registration.

    POST:
    Registers a new user with the 'PASSENGER' role.
    Validates input data, handles duplicate users, and returns user 
    details on success.
    """
    def post(self, request):
        """
        Handle user registration.
        Validates and creates a new user with the 'PASSENGER' role.
        Returns user details on success.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        role = Role.objects.get(name=Role.PASSENGER)
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            role=role,
            password=make_password(validated_data['password'])
        )
        user.save()
        data = serializer.data
        logger.info(f"{UserMessage.USER_REGISTERED_SUCCESSFULLY}username : {user.username}")
        return Response({'message': 'User registered successfully.', 
                         'user': data}, status=status.HTTP_201_CREATED)           

class LoginView(APIView):
    """
    API endpoint for user login.

    POST:
    Authenticates a user with username and password, returns JWT tokens and 
    user info, and updates last_login.
    """
    def post(self, request):
        """
        Handle user login.
        Validates credentials, authenticates user, updates last_login, and 
        returns JWT tokens and username.
        """
        try:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = self._authenticate_user(username, password)
            self._update_last_login(user)
            access_token, refresh_token = self._generate_tokens(user)
            response_data = self._build_response(user, access_token, refresh_token)

            logger.info(f"User logged in successfully: {user.username}")
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def _authenticate_user(self, username, password):
        """
        Authenticate the user with the given username and password.
        Raises an exception if credentials are invalid or user is inactive.
        Returns the authenticated user instance.
        """
        user = authenticate(username=username, password=password)
        if not user:
            raise Exception(UserMessage.INVALID_CREDENTIALS)
        if not user.is_active:
            raise Exception(UserMessage.USER_INACTIVE)
        return user

    def _update_last_login(self, user):
        """
        Update the last_login field for the user to the current time.
        """
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

    def _generate_tokens(self, user):
        """
        Generate JWT access and refresh tokens for the user.
        Returns (access_token, refresh_token).
        """
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)

    def _build_response(self, user, access_token, refresh_token):
        """
        Build the response dictionary for a successful login.
        """
        return {
            'success': True,
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.username
        }           
