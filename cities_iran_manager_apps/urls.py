# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('run_iran_city/', run, name='run_iran_city'),
    path("", province_list, name="province_list"),
    path("province/new/", province_create, name="province_create"),
    path("province/edit/<int:pk>/", province_edit, name="province_edit"),
    path("city/new/", city_create, name="city_create"),
    path("cities/", city_list, name="city_list"),
    path('city/edit/<int:pk>/', city_edit, name='city_edit'),
    path("get-cities/", get_cities, name="get-cities"),

]
