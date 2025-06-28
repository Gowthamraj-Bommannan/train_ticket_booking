from rest_framework import serializers
from .models import User, Role
from .exceptions import EmailAlreadyExists, UsernameAlreadyExists, MobileNumberAlreadyExists, InvalidInput
from django.core.exceptions import ValidationError as DjangoValidationError
from utils.constants import GeneralMessage, FieldValidationMessage

import re

class UserRegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(validators=[])
    username = serializers.CharField(validators=[])
    mobile_number = serializers.CharField(validators=[])
    
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

    def validate_password(self, value):
        if not value or len(value) < 8 or len(value) > 16:
            raise InvalidInput(FieldValidationMessage.PASSWORD_LONG_OR_SHORT)
        return value
    
    def create(self, validated_data):
        role = Role.objects.get(name=Role.PASSENGER)
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            mobile_number=validated_data['mobile_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password'],
            role=role
        )
        return user 