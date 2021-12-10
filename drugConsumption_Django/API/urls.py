
from django.urls import path, include
from API import views


urlpatterns = [
    path('', views.first, name='firstpage'),
    path('index/',views.index, name='home'),
    path('result/', views.result, name="result"),
    path('dataviz/',views.dataviz, name="dataviz"),
    path('corrMatF/',views.corrFeatures, name="corrMatF"),
    path('corrMatO/',views.corrOutputs, name='corrMatO'),
    path('map1/',views.map1, name='map1'),
    path('pie/',views.pie, name='pie')
]