from django.urls import path
from .views import *



urlpatterns = [
    path('api/bin_coordinates/' , bins , name = 'index'),
    path('api/start_coordinate/', start_point, name = 'index')
]