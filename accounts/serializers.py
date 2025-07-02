from rest_framework import serializers
from .models import User
from .exceptions import EmailAlreadyExists, UsernameAlreadyExists, MobileNumberAlreadyExists, InvalidInput
from django.core.exceptions import ValidationError as DjangoValidationError
from utils.constants import GeneralMessage, FieldValidationMessage, UserMessage
import re
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone

class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[])
    username = serializers.CharField(validators=[])
    mobile_number = serializers.CharField(validators=[])
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'email': {'required': True},
            'mobile_number': {'required': True},
        }

    def validate(self, attrs):
        
        try:
            self.Meta.model(**attrs).full_clean(exclude=['password'])
        except DjangoValidationError as e:
            errors = e.message_dict
            if 'username' in errors:
                raise UsernameAlreadyExists()
            if 'email' in errors:
                raise EmailAlreadyExists()
            if 'mobile_number' in errors:
                raise MobileNumberAlreadyExists()
            raise InvalidInput(f'{GeneralMessage.INVALID_INPUT}'.format(errors))
        return attrs

    def validate_mobile_number(self, value):
        if not re.match(r"^[6-9][0-9]{9}$", value):
            raise InvalidInput(FieldValidationMessage.MOBILE_INVALID)
        return value

    def validate_password(self, value):
        if not value or len(value) < 8 or len(value) > 16:
            raise InvalidInput(FieldValidationMessage.PASSWORD_LONG_OR_SHORT)
        return value
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise InvalidInput(UserMessage.USERNAME_AND_PASSWORD_REQUIRED)
        return attrs
