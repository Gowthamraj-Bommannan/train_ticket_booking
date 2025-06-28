from rest_framework import serializers
from .models import Station, Train, TrainStation
from django.utils import timezone
from .exceptions import InvalidInput, AlreadyExists
from utils.constants import TrainMessage, AlreadyExistsMessage
import re

class StationSerializer(serializers.ModelSerializer):
    """
    Serializer for Station model esnsure updated time for field
    updated_at
    Exposes: id, name, and code fields for API use.
    """

    class Meta:
        model = Station
        fields = ['id', 'name', 'code']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)

        instance.updated_at = timezone.now()
        instance.save()
        return instance

class TrainSerializer(serializers.ModelSerializer):
    """
    Serializer for Train model with custom validations on number and name.
    """

    total_seats = serializers.ReadOnlyField()

    class Meta:
        model = Train
        fields = ['id', 'name', 'number', 'compartments', 'total_seats', 
                  'from_station', 'to_station']

    def validate_number(self, value):
        """
        Validates the train number with 5 exactly 5 digits.
        """
        
        if not value:
            raise InvalidInput(TrainMessage.TRAIN_NUMBER_REQUIRED)
        
        if not re.match(r"\d{5}$", value):
            raise InvalidInput(TrainMessage.TRAIN_NUMBER_INVALID)
        
        if Train.objects.filter(number=value).exists():
            raise AlreadyExists(TrainMessage.TRAIN_ALREADY_EXISTS)
        
        return value.upper()
    
    def validate_name(self, value):
        """
        Validates train name and it should have minimal length of 5.
        """
        if not value:
            raise InvalidInput(TrainMessage.TRAIN_NAME_REQUIRED)
        if len(value.strip()) < 5:
            raise InvalidInput(TrainMessage.TRAIN_NAME_TOO_SHORT)
        if not re.match(r"[A-Za-z]", value):
            raise InvalidInput(TrainMessage.TRAIN_NAME_INVALID)
        if Train.objects.filter(name=value).exists():
            raise AlreadyExists(TrainMessage.TRAIN_ALREADY_EXISTS)
        
        return value.title()
        
            

class TrainStationSerialzier(serializers.ModelSerializer):
    train_name = serializers.ReadOnlyField(source = 'train.name')
    station_name = serializers.ReadOnlyField(source = 'station.name')

    class Meta:
        model = TrainStation
        fields = '__all__'