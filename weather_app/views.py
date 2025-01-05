from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from .handler import (WeatherHandler)
import requests
from django.contrib import messages
import json

def weather(request):
    if request.method == 'GET':
        return render(request, "weather_app/weather.html")

    if request.method == 'POST':
        city = request.POST.get('city')
        data = WeatherHandler(city).get_weather()
        if data is None:
            messages.error(request, "City not found")
            return redirect('weather')
        return render(request, "weather_app/current.html", {'current_data': data})

def forecast(request):
    if request.method == 'GET':
        return render(request, "weather_app/forecast.html")

    if request.method == 'POST':
        city = request.POST.get("city")
        current = request.POST.get('current') or False
        if current == "on": current = True
        hourly = request.POST.get('hourly') or False
        if hourly == "on": hourly = True
        days = request.POST.get('days') or 2
        data = WeatherHandler(city).get_forecast(hourly_forecast=hourly, current=current, days=days)
        if data is None:
            messages.error(request, "City not found")
            return redirect('forecast')
        return render(request, "weather_app/forecast_out.html", {'data': data, "current_data": data.get("current"), "hourly": data.get("hourly_forecast")})

def astronomy(request):
    if request.method == 'GET':
        return render(request, "weather_app/weather.html")

    if request.method == 'POST':
        city = request.POST.get('city')
        data = WeatherHandler(city).get_astronomy()
        print(data)
        if data is None:
            messages.error(request, "City not found")
            return redirect('astronomy')
        return render(request, "weather_app/astronomy_out.html", {'data': data})