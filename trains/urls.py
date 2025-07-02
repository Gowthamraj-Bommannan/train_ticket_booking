from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, TrainViewSet, TrainStationViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'trains', TrainViewSet)
router.register(r'train-stations', TrainStationViewSet)

# Custom views for delete-all-stops and delete-stop
trainstation_delete_all_stops = TrainStationViewSet.as_view({'delete': 'delete_all_stops'})
trainstation_delete_stop = TrainStationViewSet.as_view({'delete': 'delete_stop'})

urlpatterns = [
    path('admin/', include(router.urls)),
    path('admin/train-stations/train/<str:pk>/delete-all-stops/', trainstation_delete_all_stops, name='trainstation-delete-all-stops'),
    path('admin/train-stations/train/<str:train_number>/station/<str:station_code>/delete-stop/', trainstation_delete_stop, name='trainstation-delete-stop'),
]