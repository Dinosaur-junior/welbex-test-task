# -*- coding: utf-8 -*-
# Written by Dinosaur
#                __
#               / _)
#      _.----._/ /
#     /         /
#  __/ (  | (  |
# /__.-'|_|--|_|


# ---------------------------------------------------------------------------------------------------------------------
# import libraries
from django.urls import path

from .api import *
from .views import *

# ---------------------------------------------------------------------------------------------------------------------
# URL patterns

urlpatterns = [
    # global
    path('', index, name='delivery_main'),
    path('search', search, name='search'),

    # cargo
    path('cargo', cargo, name='cargo_main'),
    path('new_cargo', new_cargo, name='new_cargo'),
    path('delete_cargo/<int:cargo_id>/', delete_cargo, name='delete_cargo'),
    path('cargo_info/<int:cargo_id>/', cargo_info, name='cargo_info'),
    path('edit_cargo/<int:cargo_id>/', edit_cargo, name='edit_cargo'),

    # cars
    path('cars', cars, name='cars_main'),
    path('new_car', new_car, name='new_car'),
    path('delete_car/<int:car_id>/', delete_car, name='delete_car'),
    path('car_info/<int:car_id>/', car_info, name='car_info'),
    path('edit_car/<int:car_id>/', edit_car, name='edit_car'),

    # locations
    path('locations', locations, name='locations_main'),
    path('new_location', new_location, name='new_location'),
    path('delete_location/<int:location_id>/', delete_location, name='delete_location'),
    path('location_info/<int:location_id>/', location_info, name='location_info'),
    path('edit_location/<int:location_id>/', edit_location, name='edit_location'),

    # ------------------------------------------------------
    # API

    # search
    path('api/search', api_search),

    # cargo
    path('api/cargo', api_cargo),
    path('api/new_cargo', api_new_cargo),
    path('api/delete_cargo/<int:cargo_id>/', api_delete_cargo),
    path('api/cargo_info/<int:cargo_id>/', api_cargo_info),
    path('api/edit_cargo/<int:cargo_id>/', api_edit_cargo),

    # cars
    path('api/cars', api_cars),
    path('api/new_car', api_new_car),
    path('api/delete_car/<int:car_id>/', api_delete_car),
    path('api/car_info/<int:car_id>/', api_car_info),
    path('api/edit_car/<int:car_id>/', api_edit_car),

    # locations
    path('api/locations', api_locations),
    path('api/new_location', api_new_location),
    path('api/delete_location/<int:location_id>/', api_delete_location),
    path('api/location_info/<int:location_id>/', api_location_info),
    path('api/edit_location/<int:location_id>/', api_edit_location),

]
