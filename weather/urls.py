from __future__ import annotations

from django.urls import path

from .views import WeatherHistoryView, WeatherHomeView

app_name = 'weather'

urlpatterns = [
    path('', WeatherHomeView.as_view(), name='home'),
    path('history/', WeatherHistoryView.as_view(), name='history'),
]
