from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from django.db import models
from .models import Station, Train, TrainStation
from .serializers import StationSerializer, TrainSerializer, TrainStationSerialzer
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .exceptions import (DoesNotExists, InvalidInput, QueryParameterMissing
                         , AlreadyExists, NotFound)
from utils.constants import (StationMessage, TrainMessage, GeneralMessage, 
                             TrainStationMessage)
from django.db import transaction
import logging

logger = logging.getLogger('request_logger')

class StationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations for stations.

    Custom endpoints:
        - `GET /api/admin/stations/by-name/?name=<name>`:
            Retrieves station by partial/full name.
        
        - `GET /api/admin/stations/by-code/?code=<code>`:
            Retrieves station by exact code.
    """
     
    queryset = Station.objects.filter(is_active=True)
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter] # Adding search filter
    serach_fields = ['name'] # Allows searching on name field


    @action(detail=False,methods=['get'], url_path='by-name')
    def get_by_name(self, request):
        """
        Search for stations by name (case-insensitive, partial allowed).
        Returns all matching stations.
        Example: ?name=salem or ?name=Salem Junction
        """
        logger.info(f"Request to search stations by name: {request.query_params}")
        name = request.query_params.get('name', '').strip()
        if not name:
            logger.warning("Station name not provided.")
            raise InvalidInput(StationMessage.STATION_CODE_REQUIRED)
        stations = Station.objects.filter(name__icontains=name, is_active=True)
        if not stations.exists():
            logger.info(f"No station found with name containing: {name}")
            raise DoesNotExists(StationMessage.STATION_NOT_FOUND)
        serializer = self.get_serializer(stations, many=True)
        logger.info(f"Found {stations.count()} stations matching name: {name}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='by-code')
    def get_by_code(self, request):
        """
        Search for a station by exact code (case-insensitive).
        Example: ?code=MAS
        """
        logger.info(f"Request to search station by code: {request.query_params}")
        code = request.query_params.get('code', '').strip()
        if not code:
            logger.warning("Station code not provided in query.")
            raise InvalidInput(StationMessage.STATION_CODE_REQUIRED)
        station = Station.objects.filter(code__iexact=code, 
                                         is_active=True).first()
        if not station:
            logger.info(f"No station found with code: {code}")
            raise DoesNotExists(StationMessage.STATION_NOT_FOUND)
        serializer = self.get_serializer(station)
        logger.info(f"Station found with code {code}: {station.name}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft-delete a station by setting its is_active flag to False.
        """
        instance = self.get_object()
        logger.info(f"Request to delete station: {instance.name} (ID: {instance.id})")
        instance.is_active = False
        instance.save()
        logger.info(f"Station deleted successfully: {instance.name} (ID: {instance.id})")
        return Response({'succes' : True,
                         'message' : StationMessage.STATION_DELETED_SUCCESSFULLY},
                         status=status.HTTP_204_NO_CONTENT)
    

class TrainViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations for trains.

    Core Features:
    - Create, retrieve, update, and soft-delete train records.
    - Returns only active trains by default.
    - Restricted to authenticated admin users only.
    """
    queryset = Train.objects.filter(is_active=True)
    serializer_class = TrainSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


    @action(detail=False, methods=['get'], url_path='by-number')
    def search_by_number(self, request):
        """
        Search for a train using the train number.
        Example: ?number=12345
        """
        number = request.query_params.get('number', None)
        if not number:
            raise QueryParameterMissing(GeneralMessage.QUERY_MISSING)

        try:
            train = Train.objects.get(number=number)
        except Train.DoesNotExist:
            raise DoesNotExists(TrainMessage.TRAIN_NOT_FOUND)

        serializer = self.get_serializer(train)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft-delete a train by setting its is_active flag to False.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'succes' : True,
                         'message' : StationMessage.STATION_DELETED_SUCCESSFULLY},
                         status=status.HTTP_204_NO_CONTENT)
    
class TrainStationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage train stops (stations) within a train route.

    Core Features:
    - Add, update, and soft-delete individual or all stops in a train's route.
    - Supports automatic stop number assignment and reordering logic.
    - Provides endpoints to fetch stops by train number.
    - Restricted to authenticated admin users only.
    """
    queryset = TrainStation.objects.filter(is_active=True)
    serializer_class = TrainStationSerialzer
    permission_classes = [IsAdminUser, IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add-stop')
    def add_stop(self, request):
        """
        Add a station stop to a train's route, optionally specifying the stop number.
        """

        try:
            train, station, arrival_time, departure_time, stop_number = self._validate_create_route_input(request.data)
            self._validate_no_active_stop(train, station)
            train_station = self._create_train_stop(train, station, arrival_time, departure_time, stop_number)
            serializer = self.get_serializer(train_station)
            return self._build_create_route_response(serializer)
        except Exception as e:
            return self._build_create_route_error_response(e)

    def _validate_create_route_input(self, data):
        """
        Validate and extract train, station, and timing information from the request data.
        """
        train_number = data.get('train')
        station_id = data.get('station')
        arrival_time = data.get('arrival_time')
        departure_time = data.get('departure_time')
        stop_number = data.get('stop_number')
        if not all([train_number, station_id, arrival_time, departure_time]):
            raise InvalidInput(TrainStationMessage.ROUTE_VALIDATION_REQUIREMENTS)
        try:
            train = Train.objects.get(number=train_number)
        except Train.DoesNotExist:
            raise NotFound(TrainMessage.TRAIN_WITH_NUMBER_NOT_EXIST.FORMAT(
                train_number=train_number
            ))
        try:
            station = Station.objects.get(pk=station_id, is_active=True)
        except Station.DoesNotExist:
            raise NotFound(StationMessage.STATION_WITH_ID_NOT_EXISTS.format(
                station_id=station_id
            ))
        if arrival_time >= departure_time:
            raise InvalidInput(TrainStationMessage.TRAIN_STATION_DEPARTURE_MUST_GREATER)
        return train, station, arrival_time, departure_time, stop_number

    def _validate_no_active_stop(self, train, station):
        """
        Ensure no existing active stop exists for the same train-station pair.
        """
        if TrainStation.objects.filter(train=train, station=station, is_active=True).exists():
            raise AlreadyExists(TrainStationMessage.TRAIN_ROUTE_EXISTS)

    def _create_train_stop(self, train, station, arrival_time, departure_time, stop_number):
        """
        Create a new train stop with proper stop_number sequencing using atomic transaction.
        """
        with transaction.atomic():
            if stop_number is None:
                last_stop = TrainStation.objects.filter(train=train, is_active=True).order_by('-stop_number').first()
                stop_number = 1 if last_stop is None else last_stop.stop_number + 1
            else:
                stop_number = int(stop_number)
                TrainStation.objects.filter(train=train, is_active=True, stop_number__gte=stop_number).update(
                    stop_number=models.F('stop_number') + 1
                )
            return TrainStation.objects.create(
                train=train,
                station=station,
                arrival_time=arrival_time,
                departure_time=departure_time,
                stop_number=stop_number
            )

    def _build_create_route_response(self, serializer):
        """
        Build a standard success response for stop creation.
        """
        return Response({'success': True, 
                         'message': TrainStationMessage.TRAIN_STOP_ADDED, 
                         'data': serializer.data})

    def _build_create_route_error_response(self, error):
        """
        Raise exception with error message for stop creation failure.
        """
        raise Exception({'success': False,
                         'error': str(error)}, 
                         status=500)
    
    @action(detail=True, methods=['patch'], url_path='update-stop')
    def update_stop(self, request, pk=None):
        """
        Partially update a specific train stop's arrival/departure or stop number.
        """
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'success': True, 
                             'message': TrainStationMessage.STOP_UPDATED_SUCCESSFULLY, 
                             'data': serializer.data})
        except Exception as e:
            raise InvalidInput({'success': False, 
                             'error': str(e)})

    
    def destroy(self, request, *args, **kwargs):
        """
        Soft-delete a train stop by marking it inactive.
        """
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'succes' : True,
                         'message' : TrainStationMessage.TRAIN_STOP_DELETED},
                         status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='by-train')
    def get_stops_by_train(self, request):
        """
        Get all stops for a train, ordered by stop_number.
        Usage: /api/admin/train-stations/by-train/?train_number=34722
        Only active stops and active stations are shown.
        """
        train_number = request.query_params.get('train_number')
        if not train_number:
            raise InvalidInput({'success': False, 
                             'error': TrainMessage.TRAIN_QUERY_MISSING})
        try:
            train = Train.objects.get(number=train_number)
        except Train.DoesNotExist:
            raise NotFound({'success': False, 
                             'error': TrainMessage.TRAIN_WITH_NUMBER_NOT_EXIST.
                             format(
                                 train_number=train_number
                             )})
        stops = TrainStation.objects.filter(train=train, is_active=True, station__is_active=True).order_by('stop_number')
        serializer = self.get_serializer(stops, many=True)
        return Response({'success': True, 
                         'data': serializer.data},
                         status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'], url_path='train/(?P<train_number>[^/]+)/station/(?P<station_code>[^/]+)/delete-stop', url_name='delete-stop')
    def delete_stop(self, request, train_number=None, station_code=None):
        """
        Soft delete a stop for a train using train_number and station_code from the URL.
        After deletion, re-number the remaining stops for the train.
        Example: DELETE /api/admin/train-stations/train/<train_number>/station/<station_code>/delete-stop/
        """
        if not train_number or not station_code:
            raise InvalidInput({'success': False, 
                             'error': TrainStationMessage.
                             TRAIN_NUMBER_STNCODE_REQUIRED})
        try:
            train = Train.objects.get(number=train_number)
        except Train.DoesNotExist:
            raise NotFound({'success': False, 
                             'error': TrainMessage.TRAIN_WITH_NUMBER_NOT_EXIST.
                             format(
                                 train_number=train_number
                             )})
        try:
            station = Station.objects.get(code__iexact=station_code)
        except Station.DoesNotExist:
            return NotFound({'success': False, 'error': StationMessage.STATION_WITH_CODE_NOT_EXISTS
                             .format(
                                 station_code=station_code
                             )})
        try:
            stop = TrainStation.objects.get(train=train, station=station, is_active=True)
        except TrainStation.DoesNotExist:
            return NotFound({'success': False,
                             'error': TrainStationMessage.TRAIN_STOP_NOT_EXISTS.format(
                                 train_number=train_number,
                                 station_code=station_code
                             )})
        # Soft delete
        stop.is_active = False
        stop.save()
        # Re-number remaining stops
        active_stops = TrainStation.objects.filter(train=train, is_active=True).order_by('stop_number')
        for idx, s in enumerate(active_stops, start=1):
            if s.stop_number != idx:
                s.stop_number = idx
                s.save(update_fields=['stop_number'])
        return Response({'success': True, 
                         'message': TrainStationMessage.TRAIN_STOP_DELETED.format(
                             station_code=station_code
                         )}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['delete'], url_path='delete-all-stops', url_name='delete-all-stops')
    def delete_all_stops(self, request, pk=None):
        """
        Soft delete all stops for a train using train_number in the URL.
        Example: DELETE /api/admin/train-stations/train/<train_number>/delete-all-stops/
        """
        train_number = pk
        if not train_number:
            return InvalidInput({'success': False, 
                             'error': TrainMessage.TRAIN_NUMBER_REQUIRED})
        try:
            train = Train.objects.get(number=train_number)
        except Train.DoesNotExist:
            raise NotFound({'success': False, 
                             'error': TrainMessage.TRAIN_WITH_NUMBER_NOT_EXIST.format(
                                 train_number=train_number
                             )})
        stops = TrainStation.objects.filter(train=train, is_active=True)
        count = stops.count()
        stops.update(is_active=False)
        return Response({'success': True, 
                         'message': TrainStationMessage.TRAIN_ROUTE_DELETED.format(
                             count=count,
                             train_number=train_number
                         )}, 
                         status=204)