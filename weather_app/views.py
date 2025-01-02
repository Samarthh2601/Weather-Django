from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .weather_secrets import API_KEY
from .response_formatter import format_response
import requests

def get_weather(city) -> dict | None:
    url = f"{settings.WEATHER_BASE_URL}/current.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    return data

def weather(request):
    if request.method == 'GET':
        return render(request, "weather_app/weather.html")

    if request.method == 'POST':
        city = request.POST['city']
        data = get_weather(city)
        if data is None:
            return HttpResponse("Error fetching data")
        formatted_data = format_response(data)
        return render(request, "weather_app/out.html", {'data': formatted_data})
