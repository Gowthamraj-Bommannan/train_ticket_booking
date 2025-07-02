from rest_framework import serializers
from .models import Station, Train, TrainStation
from django.utils import timezone
from accounts.exceptions import InvalidInput, AlreadyExists, NotFound
from utils.constants import TrainMessage, StationMessage, TrainStationMessage
import re
from django.db import models, transaction

class StationSerializer(serializers.ModelSerializer):
    """
    Serializer for Station model esnsure updated time for field
    updated_at
    Exposes: id, name, and code fields for API use.
    """

    class Meta:
        model = Station
        fields = ['id', 'name', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators = []

    def create(self, validated_data):
        name = validated_data.get('name')
        code = validated_data.get('code')        
        # Check for case-insensitive duplicates
        if Station.objects.filter(name__iexact=name).exists():
            raise AlreadyExists(StationMessage.STATION_ALREADY_EXISTS)
        if Station.objects.filter(code__iexact=code).exists():
            raise AlreadyExists(StationMessage.STATION_ALREADY_EXISTS)
        
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.code = validated_data.get('code', instance.code)
        instance.updated_at = timezone.now()
        instance.save()
        return instance
    
    def validate_name(self, value):
        """
        Validates station name field.
        """
        if not value:
            raise InvalidInput(StationMessage.STATION_NAME_REQUIRED)
        if len(value.strip()) < 3:
            raise InvalidInput(StationMessage.STATION_NAME_TOO_SHORT)
        if Station.objects.filter(name=value).exists():
            raise AlreadyExists(StationMessage.STATION_ALREADY_EXISTS)
        return value.strip()
    
    def validate_code(self, value):
        """
        Validates station code field.
        """
        if not value:
            raise InvalidInput(StationMessage.STATION_CODE_REQUIRED)
        if len(value.strip()) < 2:
            raise InvalidInput(StationMessage.STATION_CODE_TOO_SHORT)
        if Station.objects.filter(code=value).exists():
            raise AlreadyExists(StationMessage.STATION_ALREADY_EXISTS)
        return value.strip().upper()

class TrainSerializer(serializers.ModelSerializer):
    """
    Serializer for Train model with custom validations on number and name.
    """

    total_seats = serializers.ReadOnlyField()
    number = serializers.ReadOnlyField()
    from_station_name = serializers.CharField(source='from_station.name', 
                                              read_only=True)
    to_station_name = serializers.CharField(source='to_station.name', 
                                            read_only=True)

    class Meta:
        model = Train
        fields = ['id', 'name', 'number', 'from_station_name', 'to_station_name',
                  'total_seats', 'from_station', 'to_station']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].validators = []
    
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
    
    def create(self, validated_data):
        name = validated_data.get('name')
        if Train.objects.filter(name__iexact=name).exists():
            raise AlreadyExists(TrainMessage.TRAIN_ALREADY_EXISTS)
        return super().create(validated_data)
    
    def validate(self, data):
        # from_station should not be same as to_station
        from_station = data.get('from_station')
        to_station = data.get('to_station')
        if from_station and to_station and from_station == to_station:
            raise InvalidInput("From and To stations must be different.")
        return data
    
class TrainStationStopSerializer(serializers.Serializer):
    station = serializers.PrimaryKeyRelatedField(queryset=Station.objects.filter(is_active=True))
    arrival_time = serializers.TimeField()
    departure_time = serializers.TimeField()

    def validate(self, data):
        if data['arrival_time'] >= data['departure_time']:
            raise InvalidInput(TrainStationMessage.TRAIN_STATION_DEPARTURE_MUST_GREATER)
        return data

    def validate_station(self, value):
        # Get train from context if available
        train = self.context.get('train')
        if train and TrainStation.objects.filter(train=train, station=value, is_active=True).exists():
            raise AlreadyExists(TrainStationMessage.STATION_EXIST_IN_ROUTE)
        return value

class TrainStationSerialzer(serializers.ModelSerializer):
    """
    Serializer for creating train routes and viewing individual train stops.

    - For `POST`, use the `stops` field to provide a list of station stops (bulk add), or a single stop object (single add).
    - For `GET`, it will display the details of a single train stop.
    """
    train = serializers.CharField(write_only=True)  # Accept train number as input
    train_name = serializers.CharField(source='train.name', read_only=True)
    station_name = serializers.CharField(source='station.name', read_only=True)
    stops = TrainStationStopSerializer(many=True, write_only=True, required=False)
    stop_number = serializers.IntegerField(required=False)

    class Meta:
        model = TrainStation
        fields = [
            'id', 'train', 'train_name', 'station', 'station_name',
            'arrival_time', 'departure_time', 'stop_number', 'stops'
        ]

    def to_representation(self, instance):
        # Only show active stops and active stations
        if not instance.is_active or not instance.station.is_active:
            return None
        return super().to_representation(instance)

    def validate(self, attrs):
        # Resolve train number to Train instance at the root level
        train_number = self.initial_data.get('train')
        if not train_number:
            raise InvalidInput("Train number is required.")
        try:
            train = Train.objects.get(number=train_number)
        except Train.DoesNotExist:
            raise InvalidInput(f"Train with number '{train_number}' does not exist.")
        attrs['train'] = train
        # If single add, check for active stop conflict
        station = self.initial_data.get('station')
        if station:
            if TrainStation.objects.filter(train=train, station=station, is_active=True).exists():
                raise AlreadyExists(TrainStationMessage.STATION_EXIST_IN_ROUTE)
        return attrs

    def validate_station(self, value):
        # Only check for single add (not bulk)
        train_number = self.initial_data.get('train')
        if train_number:
            try:
                train = Train.objects.get(number=train_number)
            except Train.DoesNotExist:
                raise InvalidInput(f"Train with number '{train_number}' does not exist.")
            if TrainStation.objects.filter(train=train, station=value, is_active=True).exists():
                raise AlreadyExists(TrainStationMessage.STATION_EXIST_IN_ROUTE)
        return value
        
