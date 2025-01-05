from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.weather, name='weather'),
    path('forecast/', views.forecast, name='forecast'),
    path('astronomy', views.astronomy, name='astronomy'),
]