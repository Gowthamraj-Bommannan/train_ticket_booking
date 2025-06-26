from rest_framework import serializers
from .models import User, Role
from .exceptions import EmailAlreadyExists, UsernameAlreadyExists, MobileNumberAlreadyExists, InvalidInput
import re

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'mobile_number', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'email': {'required': True},
            'mobile_number': {'required': True},
        }

    def validate_email(self, value):
        if not value:
            raise InvalidInput('Email is required.')
        value = value.lower()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise InvalidInput('Invalid email format.')
        if User.objects.filter(email=value).exists():
            raise EmailAlreadyExists()
        return value

    def validate_username(self, value):
        if not value:
            raise InvalidInput('Username is required.')
        value = value.lower()
        if len(value) < 3:
            raise InvalidInput('Username must be at least 3 characters long.')
        if User.objects.filter(username=value).exists():
            raise UsernameAlreadyExists()
        return value

    def validate_mobile_number(self, value):
        if not value:
            raise InvalidInput('Mobile number is required.')
        if not re.match(r"^[6-9][0-9]{9}$", value):
            raise InvalidInput('Mobile number must be 10 digits and starts with 6 to 9.')
        if User.objects.filter(mobile_number=value).exists():
            raise MobileNumberAlreadyExists()
        return value

    def validate_first_name(self, value):
        if not value:
            raise InvalidInput('First name is required.')
        return value

    def validate_password(self, value):
        if not value or len(value) < 8 or len(value) > 16:
            raise InvalidInput('Password must be 8 to 16 characters long.')
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