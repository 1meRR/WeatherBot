from __future__ import annotations

from django.contrib import admin

from .models import WeatherRequest


@admin.register(WeatherRequest)
class WeatherRequestAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'description', 'requested_at', 'user')
    search_fields = ('city', 'description', 'user__username')
    list_filter = ('requested_at',)
