from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StationViewSet, TrainViewSet

router = DefaultRouter()
router.register(r'stations', StationViewSet)
router.register(r'trains', TrainViewSet)

urlpatterns = [
    path('admin/', include(router.urls))
]
