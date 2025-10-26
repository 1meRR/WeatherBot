from __future__ import annotations

from django.conf import settings
from django.db import models


class WeatherRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='weather_requests',
    )
    city = models.CharField(max_length=255)
    temperature = models.FloatField()
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=8, blank=True)
    requested_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-requested_at']
        verbose_name = 'Weather request'
        verbose_name_plural = 'Weather requests'

    def __str__(self) -> str:
        return f"{self.city} @ {self.requested_at:%Y-%m-%d %H:%M}"
