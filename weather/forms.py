from __future__ import annotations

from django import forms


class WeatherSearchForm(forms.Form):
    city = forms.CharField(
        label='City',
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'City name'}),
    )
