from __future__ import annotations

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import WeatherRequest
from .serializers import WeatherResponseSerializer, WeatherRequestSerializer
from .services import WeatherAPIError, fetch_weather


class WeatherViewSet(viewsets.ViewSet):
    permission_classes = (permissions.AllowAny,)

    def list(self, request: Request) -> Response:
        city = request.query_params.get('city')
        if not city:
            return Response({'detail': 'city parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            weather = fetch_weather(city)
        except WeatherAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        WeatherRequest.objects.create(
            user=request.user if request.user.is_authenticated else None,
            city=weather.city,
            temperature=weather.temperature,
            description=weather.description,
            icon=weather.icon,
        )

        serializer = WeatherResponseSerializer(weather.__dict__)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=(permissions.IsAuthenticated,))
    def history(self, request: Request) -> Response:
        queryset = WeatherRequest.objects.filter(user=request.user)
        data = WeatherRequestSerializer(queryset, many=True).data
        return Response(data)
