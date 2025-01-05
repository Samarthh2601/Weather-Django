from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('current/', views.current, name='current'),
    path('forecast/', views.forecast, name='forecast'),
    path('astronomy/', views.astronomy, name='astronomy'),
]