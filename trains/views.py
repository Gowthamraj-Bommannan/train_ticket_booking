from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from .models import Station, Train
from .serializers import StationSerializer, TrainSerializer
from .permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .exceptions import DoesNotExists, InvalidInput
from utils.constants import StationMessage

class StationViewSet(viewsets.ModelViewSet):
    """
    ViewSet to manage CRUD operations for stations.

    - List all active stations: `GET /api/admin/stations/`
    - Create new station: `POST /api/admin/stations/`
    - Update existing station: `PUT/PATCH /api/admin/stations/<id>/`
    - Delete station (soft-delete recommended): `DELETE /api/admin/stations/<id>/`

    Custom endpoints:
        - `GET /api/admin/stations/by-name/?name=<name>`:
            Retrieves station by partial/full name (case-insensitive).
        
        - `GET /api/admin/stations/by-code/?code=<code>`:
            Retrieves station by exact code (case-insensitive).
    """
     
    queryset = Station.objects.filter(is_active=True)
    serializer_class = StationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter] # Adding search filter
    serach_fields = ['name'] # Allows searching on name field


    @action(detail=False,methods=['get'], url_path='by-name')
    def get_by_name(self, request):
        """
        Search for a station by name (case-insensitive, partial allowed).
        Example: ?name=salem or ?name=Salem Junction
        """

        name = request.query_params.get('name', '').strip()
        if not name:
            raise InvalidInput(StationMessage.STATION_CODE_REQUIRED)
        station = Station.objects.filter(name__icontains=name, is_active=True).first()
        if not station:
            raise DoesNotExists(StationMessage.STATION_NOT_FOUND)
        serializer = self.get_serializer(station)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    @action(detail=False, methods=['get'], url_path='by-code')
    def get_by_code(self, request):
        """
        Search for a station by exact code (case-insensitive).
        Example: ?code=MAS
        """

        code = request.query_params.get('code', '').strip()
        if not code:
            raise InvalidInput(StationMessage.STATION_CODE_REQUIRED)
        station = Station.objects.filter(code__iexact=code, is_active=True).first()
        if not station:
            raise DoesNotExists(StationMessage.STATION_NOT_FOUND)
        serializer = self.get_serializer(station)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response({'succes' : True,
                         'message' : StationMessage.STATION_DELETED_SUCCESSFULLY},
                         status=status.HTTP_204_NO_CONTENT)
    

class TrainViewSet(viewsets.ModelViewSet):
    queryset = Train.objects.filter(is_active=True)
    serializer_class = TrainSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]

    def list(self, request, *args, **kwargs):
        try:
            return super().list(request, *args, **kwargs)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'success': False, 'error': str(e)}, status=500)

    