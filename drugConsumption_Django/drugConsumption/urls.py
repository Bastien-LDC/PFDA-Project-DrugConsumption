
from django.contrib import admin
from django.urls import path, include
from API import views

urlpatterns = [
    path('', include('API.urls'))
]
