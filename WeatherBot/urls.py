from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from weather.api import WeatherViewSet
from users.api import UserViewSet, LoginView

router = routers.DefaultRouter()
router.register('weather', WeatherViewSet, basename='weather')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/', include(router.urls)),
    path('', include('weather.urls')),
]
