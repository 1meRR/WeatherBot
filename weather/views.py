from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .forms import WeatherSearchForm
from .models import WeatherRequest
from .services import WeatherAPIError, fetch_weather


class WeatherHomeView(TemplateView):
    template_name = 'weather/home.html'

    def get(self, request, *args, **kwargs):  # type: ignore[override]
        form = WeatherSearchForm(request.GET or None)
        context: dict[str, object] = {'form': form, 'result': None}
        if form.is_bound and form.is_valid():
            city = form.cleaned_data['city']
            try:
                result = fetch_weather(city)
            except WeatherAPIError as exc:
                messages.error(request, str(exc))
            else:
                WeatherRequest.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    city=result.city,
                    temperature=result.temperature,
                    description=result.description,
                    icon=result.icon,
                )
                context['result'] = result
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class WeatherHistoryView(TemplateView):
    template_name = 'weather/history.html'

    def get_context_data(self, **kwargs):  # type: ignore[override]
        context = super().get_context_data(**kwargs)
        context['history'] = WeatherRequest.objects.filter(user=self.request.user)
        return context
