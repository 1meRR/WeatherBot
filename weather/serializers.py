from __future__ import annotations

from rest_framework import serializers

from .models import WeatherRequest


class WeatherResponseSerializer(serializers.Serializer):
    city = serializers.CharField()
    temperature = serializers.FloatField()
    description = serializers.CharField()
    icon = serializers.CharField(allow_blank=True)


class WeatherRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRequest
        fields = ('id', 'city', 'temperature', 'description', 'icon', 'requested_at')
        read_only_fields = fields
