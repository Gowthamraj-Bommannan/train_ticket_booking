from django.urls import path
from .views import RegisterView, LoginView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] 